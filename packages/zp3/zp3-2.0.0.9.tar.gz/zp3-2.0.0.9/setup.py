# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zp3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zp3',
    'version': '2.0.0.9',
    'description': 'Example Package for Zühlke Python Course',
    'long_description': None,
    'author': 'Iwan Silvan Bolzern',
    'author_email': 'iwan.bolzern@bluewin.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
