# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polypuppet', 'polypuppet.agent', 'polypuppet.server']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'configparser>=5.0.2,<6.0.0',
 'protobuf>=3.15.7,<4.0.0',
 'requests-html>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['polypuppet = polypuppet.agent.cli:cli',
                     'polypuppet-autosign = polypuppet.agent.cli:autosign']}

setup_kwargs = {
    'name': 'polypuppet',
    'version': '0.1.1',
    'description': 'Administration tool for SPBSTU',
    'long_description': None,
    'author': 'LLDay',
    'author_email': 'ssdenis99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
