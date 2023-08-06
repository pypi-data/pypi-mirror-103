# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cabin',
 'cabin.domain',
 'cabin.domain.messages',
 'cabin.domain.tables',
 'cabin.utils']

package_data = \
{'': ['*']}

install_requires = \
['flatten-json>=0.1.13,<0.2.0',
 'marshmallow-dataclass[enum]>=8.4.1,<9.0.0',
 'marshmallow>=3.11.1,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'cabin',
    'version': '0.2.0',
    'description': 'Common code for log-cabin-data projects',
    'long_description': '# cabin\n\nA library containing common Python code for log-cabin-data projects.\n',
    'author': 'Finn Welsford-Ackroyd',
    'author_email': 'finnwa24@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
