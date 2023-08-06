# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['npmrc2yarnrc']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'mergedeep>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['npmrc2yarnrc = '
                     'npmrc2yarnrc.__init__:merge_iotex_npmrc_into_yarnrc']}

setup_kwargs = {
    'name': 'npmrc2yarnrc',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
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
