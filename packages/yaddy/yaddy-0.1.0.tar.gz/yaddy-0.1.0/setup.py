# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaddy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['accept = behave.__main__:main',
                     'unit = pytest:console_main']}

setup_kwargs = {
    'name': 'yaddy',
    'version': '0.1.0',
    'description': 'Yet Another Domain (Driven) Development librarY for Python',
    'long_description': None,
    'author': 'S. Guliaev',
    'author_email': 'dev.sagul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
