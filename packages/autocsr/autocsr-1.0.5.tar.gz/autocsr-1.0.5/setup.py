# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autocsr', 'autocsr.protos']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'cryptography>=3.4.7,<4.0.0',
 'protobuf>=3.15.8,<4.0.0',
 'pyOpenSSL>=20.0.1,<21.0.0',
 'pyasn1-modules>=0.2.8,<0.3.0',
 'python-pkcs11>=0.7.0,<0.8.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['autocsr = autocsr.cli:main']}

setup_kwargs = {
    'name': 'autocsr',
    'version': '1.0.5',
    'description': '',
    'long_description': None,
    'author': 'Max Wolfe',
    'author_email': 'max@securitywolfe.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
