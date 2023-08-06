from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField

MODEL_DONE_ERROR_MSG = _("Models marked as done can not be edited anymore.")


class ModelDoneError(Exception):
    def __init__(self, msg=MODEL_DONE_ERROR_MSG, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class CreatedModifiedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SlugifiedModel(models.Model):
    slug = models.SlugField(editable=False, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ParentManager(models.Manager):
    def get_roots(self):
        return Parent.objects.filter(parent=None)


class Parent(CreatedModifiedModel, SlugifiedModel):
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    parent = models.ForeignKey(
        "Parent",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="child_parents",
    )
    objects = ParentManager()

    class Meta:
        ordering = ["name", "active"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.active = self.parent.active
        super().save(*args, **kwargs)

    @property
    def debit(self):
        return self.get_sum("debit")

    @property
    def credit(self):
        return self.get_sum("credit")

    def get_sum(self, column):
        """Returns the sum of direct child accounts and child parents."""
        account_sum = Entry.objects.filter(
            account__parent=self, virtual=False
        ).aggregate(Sum(column))[f"{column}__sum"]
        account_sum = account_sum if account_sum is not None else Decimal(0.0)
        parent_sum = sum([p.get_sum(column) for p in self.child_parents.all()])
        parent_sum = parent_sum if parent_sum is not None else Decimal(0.0)
        value = account_sum + parent_sum
        return value


class Account(CreatedModifiedModel, SlugifiedModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "Parent",
        on_delete=models.PROTECT,
        related_name="child_accounts",
    )
    virtual = models.BooleanField(default=False)

    class Meta:
        unique_together = [["name", "parent"]]

    @property
    def active(self):
        return self.parent.active

    @property
    def debit(self):
        return self.get_entry_sum("debit")

    @property
    def credit(self):
        return self.get_entry_sum("credit")

    def get_entry_sum(self, column):
        value = Entry.objects.filter(account=self, virtual=self.virtual).aggregate(
            Sum(column)
        )[f"{column}__sum"]
        return value if value is not None else Decimal(0.0)


class BookingManager(models.Manager):
    def bulk_import(self, entries, account):
        """
        Bulk imports entries and create a new booking for each entry.
        ":param entries: Entries to be imported (list of dicts)
        """
        bookings = []
        for entry in entries:
            booking = self.create()
            booking.text = entry.pop("text")
            entry["account"] = account
            entry["booking"] = booking
            entry = Entry.objects.create(**entry)
            bookings.append(booking)
        return bookings


class BookingDocument(models.Model):
    booking = models.ForeignKey(
        "Booking",
        on_delete=models.PROTECT,
        related_name="documents",
    )
    document = models.ForeignKey(
        "doma.Document",
        on_delete=models.PROTECT,
        related_name="bookings",
    )


class Booking(CreatedModifiedModel):
    done = models.BooleanField(default=False)
    text = models.TextField()

    __done = None

    objects = BookingManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__done = self.done

    @property
    def debit(self):
        return self.get_entry_sum("debit")

    @property
    def credit(self):
        return self.get_entry_sum("credit")

    def get_entry_sum(self, column):
        value = Entry.objects.filter(booking=self, virtual=False).aggregate(
            Sum(column)
        )[f"{column}__sum"]
        return value if value is not None else Decimal(0.0)

    @property
    def entry_sums_match(self):
        return self.get_entry_sum("debit") == self.get_entry_sum("credit")

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.done and self.done == self.__done:
            raise ModelDoneError()
        elif self.done and self.done != self.__done:
            if not self.entry_sums_match:
                self.done = False
                raise ValidationError(
                    _(f"Entry sums do not match up Debit {self.debit} != {self.credit}")
                )
            else:
                super().save(force_insert, force_update, *args, **kwargs)
            self.__done = self.done
        elif not self.done and self.done == self.__done:
            super().save(force_insert, force_update, *args, **kwargs)
            self.__done = self.done
        elif not self.done and self.done != self.__done:
            raise ModelDoneError()


class Entry(CreatedModifiedModel):
    account = models.ForeignKey(
        "Account", on_delete=models.PROTECT, related_name="entries"
    )
    booking = models.ForeignKey(
        "Booking", on_delete=models.PROTECT, related_name="entries"
    )
    debit = MoneyField(
        max_digits=14, decimal_places=2, default_currency="EUR", null=True, blank=True
    )
    credit = MoneyField(
        max_digits=14, decimal_places=2, default_currency="EUR", null=True, blank=True
    )
    virtual = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_either_debit_or_credit",
                check=(
                    models.Q(debit__isnull=True, credit__isnull=False)
                    | models.Q(debit__isnull=False, credit__isnull=True)
                ),
            )
        ]

    def save(self, *args, **kwargs):
        if self.done:
            raise ModelDoneError()
        else:
            super().save(*args, **kwargs)

    @property
    def done(self):
        return self.booking.done
