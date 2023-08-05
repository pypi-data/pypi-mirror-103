# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
install_requires = \
['zp3>=1,<2']

setup_kwargs = {
    'name': 'zp1',
    'version': '1.0.0.8',
    'description': 'Example Package for Zühlke Python Course',
    'long_description': None,
    'author': 'Iwan Silvan Bolzern',
    'author_email': 'iwan.bolzern@bluewin.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
