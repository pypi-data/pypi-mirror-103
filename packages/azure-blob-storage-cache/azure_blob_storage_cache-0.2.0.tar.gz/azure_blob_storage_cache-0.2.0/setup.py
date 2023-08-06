# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azure_blob_storage_cache']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.8.1,<13.0.0']

setup_kwargs = {
    'name': 'azure-blob-storage-cache',
    'version': '0.2.0',
    'description': 'Azure Blob Storage as object cache',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
