# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubernetesclustermonitor']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'kubernetesclustermonitor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kkugler',
    'author_email': 'kaikugler@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
