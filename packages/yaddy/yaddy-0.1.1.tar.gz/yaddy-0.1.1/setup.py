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
    'version': '0.1.1',
    'description': 'Yet Another Domain (Driven) Development librarY for Python',
    'long_description': '# yaddy\nYet Another Domain (Driven) Development librarY for Python\n\nWarning: This repository is in WIP (Work In Progress) state. None\nof the APIs are fixed, do not use it in your production environment.\n\nyaddy is a library that provides a basis for DDD (Domain Driven\nDevelopment) in python. It is mostly developed for my own needs,\nbut any suggestions are appreciated.\n\n## Tests\n\nHigh-level (acceptance, e2e) tests\ncould be run with:\n\n```Shell\npoetry run accept\n```\n\nDeveloper (unit) tests could be run\nwith:\n\n```Shell\npoetry run unit\n```',
    'author': 'S. Guliaev',
    'author_email': 'dev.sagul@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-yaddy/yaddy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
