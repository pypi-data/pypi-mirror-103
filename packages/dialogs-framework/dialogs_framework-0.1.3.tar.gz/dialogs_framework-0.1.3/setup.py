# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dialogs_framework', 'dialogs_framework.persistence']

package_data = \
{'': ['*']}

install_requires = \
['gevent>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'dialogs-framework',
    'version': '0.1.3',
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
