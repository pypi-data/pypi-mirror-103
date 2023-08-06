# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['doma', 'doma.migrations', 'doma.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0',
 'Pillow>=8.2.0,<9.0.0',
 'freezegun>=1.1.0,<2.0.0',
 'pdf2image>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'django-doma',
    'version': '0.2.1',
    'description': 'Simple Document Management for Django',
    'long_description': '# doma\n\n**doma** is a simple document managment app for django.\nIt provides the necessary models and view and is ready to be included into your project.\n\nDetailed documentation is in the "docs" directory.\n\n## Installation\n\nInstall `django-doma` using pip:\n\n```zsh\n$ pip install django-doma\n```\n\n## Quick start\n\n1. Add "doma" to your INSTALLED_APPS setting like this::\n\n```python\nINSTALLED_APPS = [\n    ...\n    "doma",\n]\n```\n\n2. Include the polls URLconf in your project urls.py like this::\n\n    path(\'doma/\', include(\'doma.urls\')),\n\n3. Run ``python manage.py migrate`` to create the doma models.\n\n4. Visit http://127.0.0.1:8000/doma/ to start accounting.\n',
    'author': 'Florian Rämisch',
    'author_email': 'olf@subsignal.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/olf42/django-doma',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
