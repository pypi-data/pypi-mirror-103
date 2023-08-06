# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waterdip']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'waterdip',
    'version': '0.1.0',
    'description': 'Waterdip Python SDK',
    'long_description': None,
    'author': 'Subhankar',
    'author_email': 'suhankar@waterdip.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
