# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyridy']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.3,<7.0.0']

setup_kwargs = {
    'name': 'pyridy',
    'version': '0.1.1',
    'description': 'Support library for measurements made with the Ridy Android App',
    'long_description': '# Ridy-Support-Library\n\nPython Support Library to import and process Ridy files',
    'author': 'Philipp Simon Leibner',
    'author_email': 'philip.leibner@ifs.rwth-aachen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
