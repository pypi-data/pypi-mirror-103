# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['secondmer']
setup_kwargs = {
    'name': 'secondmer',
    'version': '1.0.1',
    'description': 'SecondMer MILLIseconds. secondmer.start(100). Now library free!',
    'long_description': None,
    'author': 'TikOt Studio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
