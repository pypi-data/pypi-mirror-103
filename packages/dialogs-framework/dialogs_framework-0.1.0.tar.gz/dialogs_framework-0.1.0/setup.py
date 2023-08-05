# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialogs_framework', 'dialogs_framework.persistence']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'gevent>=21.1.2,<22.0.0',
 'mypy>=0.812,<0.813',
 'pytest>=6.2.3,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'dialogs-framework',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alon',
    'author_email': 'alon.gal@khealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
