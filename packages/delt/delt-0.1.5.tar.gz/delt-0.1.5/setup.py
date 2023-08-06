# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delt',
 'delt.bridge',
 'delt.management',
 'delt.management.commands',
 'delt.messages',
 'delt.messages.host',
 'delt.messages.postman',
 'delt.messages.postman.assign',
 'delt.messages.postman.provide',
 'delt.messages.postman.reserve',
 'delt.messages.postman.unassign',
 'delt.messages.postman.unprovide',
 'delt.messages.postman.unreserve',
 'delt.migrations',
 'delt.registry',
 'delt.service']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0',
 'PyYAML>=5.4.1,<6.0.0',
 'bergen>=0.3.76,<0.4.0',
 'django-rest-framework>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'delt',
    'version': '0.1.5',
    'description': 'A python brige to use arkitekt in your Djangop Application',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
