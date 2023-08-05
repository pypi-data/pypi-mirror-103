# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spotiapi']
install_requires = \
['http3>=0.6.7,<0.7.0']

setup_kwargs = {
    'name': 'spotiapi',
    'version': '2.0.3',
    'description': 'A small asynchronous Wrapper for Spotify Web API.',
    'long_description': None,
    'author': 'Aleksey Demchenkov',
    'author_email': 'admin@julheer.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
