# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netsuite']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3,<4', 'requests-oauthlib>=1.3,<2.0', 'zeep>=4,<5']

extras_require = \
{'all': ['authlib>=0.15.3,<0.16.0', 'httpx>=0.17,<0.18', 'ipython>=7,<8'],
 'cli': ['ipython>=7,<8'],
 'rest_api': ['authlib>=0.15.3,<0.16.0', 'httpx>=0.17,<0.18']}

entry_points = \
{'console_scripts': ['netsuite = netsuite.__main__:main']}

setup_kwargs = {
    'name': 'netsuite',
    'version': '0.6.3',
    'description': 'Wrapper around Netsuite SuiteTalk SOAP/REST Web Services and Restlets.',
    'long_description': '# netsuite\n\n[![Continuous Integration Status](https://github.com/jmagnusson/netsuite/actions/workflows/ci.yml/badge.svg)](https://github.com/jmagnusson/netsuite/actions/workflows/ci.yml)\n[![Continuous Delivery Status](https://github.com/jmagnusson/netsuite/actions/workflows/cd.yml/badge.svg)](https://github.com/jmagnusson/netsuite/actions/workflows/cd.yml)\n[![Code Coverage](https://img.shields.io/codecov/c/github/jmagnusson/netsuite?color=%2334D058)](https://codecov.io/gh/jmagnusson/netsuite)\n[![PyPI version](https://img.shields.io/pypi/v/netsuite.svg)](https://pypi.python.org/pypi/netsuite/)\n[![License](https://img.shields.io/pypi/l/netsuite.svg)](https://pypi.python.org/pypi/netsuite/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/netsuite.svg)](https://pypi.org/project/netsuite/)\n[![PyPI status (alpha/beta/stable)](https://img.shields.io/pypi/status/netsuite.svg)](https://pypi.python.org/pypi/netsuite/)\n\nMake requests to NetSuite SuiteTalk SOAP/REST Web Services and Restlets\n\n## Installation\n\nProgrammatic use only:\n\n    pip install netsuite\n\nWith NetSuite SuiteTalk REST Web Services API support:\n\n    pip install netsuite[rest_api]\n\nWith CLI support:\n\n    pip install netsuite[cli]\n\nWith all features:\n\n    pip install netsuite[all]\n\n## Documentation\n\nIs found here: https://jmagnusson.github.io/netsuite/\n',
    'author': 'Jacob Magnusson',
    'author_email': 'm@jacobian.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jmagnusson.github.io/netsuite/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
