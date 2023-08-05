# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['agilecode_test_tools']
install_requires = \
['allure-pytest==2.8.19',
 'black==20.8b1',
 'mypy==0.812',
 'pillow==8.1.0',
 'playwright==1.9.2',
 'pytest-xdist==2.1.0',
 'pytest==6.1.0',
 'requests==2.24.0']

setup_kwargs = {
    'name': 'agilecode-test-tools',
    'version': '0.4.0',
    'description': 'Package contains reusable code for api and unit tests',
    'long_description': None,
    'author': 'Vladyslav Rylov',
    'author_email': 'vladislav.rylov@agilecode.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
