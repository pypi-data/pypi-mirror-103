# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_proxbox',
 'netbox_proxbox.api',
 'netbox_proxbox.migrations',
 'netbox_proxbox.proxbox_api']

package_data = \
{'': ['*'], 'netbox_proxbox': ['templates/netbox_proxbox/*']}

setup_kwargs = {
    'name': 'netbox-proxbox',
    'version': '0.0.2',
    'description': 'Netbox Plugin - Integrate Proxmox and Netbox',
    'long_description': None,
    'author': 'Emerson Felipe',
    'author_email': 'emerson.felipe@nmultifibra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
