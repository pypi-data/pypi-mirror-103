# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookserver', 'bookserver.internal', 'bookserver.routers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'alembic>=1.4.3,<2.0.0',
 'databases[postgresql,sqlite]>=0.4.1,<0.5.0',
 'fastapi>=0.62.0,<0.63.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'uvicorn>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'bookserver',
    'version': '0.1.0',
    'description': 'A new Runestone Server Framework',
    'long_description': None,
    'author': 'Brad Miller',
    'author_email': 'bonelake@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
