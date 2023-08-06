# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parametrize']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parametrize',
    'version': '0.0.0',
    'description': 'Drop-in @pytest.mark.parametrize replacement for unittest.TestCase',
    'long_description': None,
    'author': 'MrMrRobat',
    'author_email': 'appkiller16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
