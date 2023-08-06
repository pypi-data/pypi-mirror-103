# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_bundle']

package_data = \
{'': ['*']}

install_requires = \
['applauncher>=2.0.0,<3.0.0', 'celery>=5.0.5,<6.0.0']

setup_kwargs = {
    'name': 'celery-bundle',
    'version': '2.0.0',
    'description': '',
    'long_description': None,
    'author': 'Alvaro Garcia',
    'author_email': 'maxpowel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
