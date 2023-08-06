# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['response_differ']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'deepdiff>=5.3.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'vcrpy>=4.1.1,<5.0.0']

entry_points = \
{'console_scripts': ['run = differ.cli:run']}

setup_kwargs = {
    'name': 'response-differ',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vkytepov',
    'author_email': 'vkytepov@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
