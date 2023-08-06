# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['kesha', 'kesha.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0',
 'PyYAML>=5.4.1,<6.0.0',
 'django-doma>=0.2.1,<0.3.0',
 'django-money>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'django-kesha',
    'version': '0.1.2',
    'description': 'Accounting Helper Django App',
    'long_description': '# kesha\n\nkesha is an accounting helper for django.\nIt provides the necessary models and view and is ready to be included into your project.\n\n![django_kesha_logo](assets/django-kesha-logo.png?raw=true "django-kesha-logo")\n\n## Idea\n\nI need an accounting tool, but I don\'t like Gnucash. I want to link documents to each booking,\nand the whole thing should be somewhat auditproof. I could not find any tool that suits these\nneeds, therefore I started writing my own tools. Previously I worked on [kescher](https://github.com/westnetz/kescher) which is the proof of concept for this application. It has some major flaws, (e.g. i does not calculate correctly) but this will be fixed with this app.\n\n## Features\n\n_Django-kesha_ currently provides some basic accounting functionality. \n\n## Related apps\n\n* [django-doma](https://github.com/olf42/django-doma) - Simple Document Management App\n* [django-afa](https://github.com/olf42/django-afa) - Aufwendungen für Abschreibungen Helper\n\nTested with the following versions of Python/Django:\n\n* Django: 2.2, 3.0, 3.1, 3.2\n* Python: 3.7, 3.8, 3.9\n\n## Installation\n\nInstall `django-kesha` using pip:\n\n```zsh\n$ pip install django-kesha\n```\n\n## Quick start\n\n1. Add "kesha" to your INSTALLED_APPS setting like this::\n\n```python\nINSTALLED_APPS = [\n    ...\n    "kesha",\n]\n```\n\n2. Include the polls URLconf in your project urls.py like this::\n\n    path(\'kesha/\', include(\'kesha.urls\')),\n\n3. Run ``python manage.py migrate`` to create the kesha models.\n\n4. Visit http://127.0.0.1:8000/kesha/ to start accounting.\n',
    'author': 'Florian Rämisch',
    'author_email': 'olf@subsignal.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/olf42/django-kesha',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
