# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwned']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'django-pwned-validator',
    'version': '0.0.4',
    'description': 'A PwnedPassword validator for Django',
    'long_description': "Django Pwned Passwords Validator\n================================\n\nThis package provides a password validator for Django that checks submitted\npasswords against the `Pwned Passwords API <https://haveibeenpwned.com/API/v2>`_.\n\nTo protect the security of the password being checked a range search is used. Specifically,\nonly the first 5 characters of a SHA-1 password hash are sent to the API. The\nvalidator then locally looks for the full hash in the range returned.\n\nInstallation\n~~~~~~~~~~~~\n\n.. code-block:: sh\n\n    pip install django-pwned-validator\n\nModify your `settings.py` to install the app and enable the validator:\n\n.. code-block:: python\n\n    INSTALLED_APPS = [\n        'pwned.apps.PwnedConfig',\n        ...\n    ]\n\n    AUTH_PASSWORD_VALIDATORS = [\n        {\n            'NAME': 'pwned.validators.PwnedValidator',\n        },\n        ...\n    ]\n\n\nCompatibility\n~~~~~~~~~~~~~\nSupports Django 2.2 to 3.2 on Python 3.5 to 3.8.\n",
    'author': 'Craig Loftus',
    'author_email': 'craigloftus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
