# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-quote-generator-132190312',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Santhin',
    'author_email': 'psierkin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
