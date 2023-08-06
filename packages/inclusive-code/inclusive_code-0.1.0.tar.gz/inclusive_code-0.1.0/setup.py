# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['inclusive_code']
install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'pyhumps>=1.6.1,<2.0.0', 'pylint>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'inclusive-code',
    'version': '0.1.0',
    'description': 'A custom Pylint checker to enforce an inclusive language style guide',
    'long_description': None,
    'author': 'Helen Stockman',
    'author_email': 'helen@flexport.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
