# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'squid',
    'version': '0.2.0',
    'description': 'Coming soon!',
    'long_description': None,
    'author': 'PierreGuilmin',
    'author_email': 'pierreguilmin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
