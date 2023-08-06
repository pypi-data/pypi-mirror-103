# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampharos']

package_data = \
{'': ['*'], 'ampharos': ['data/*']}

install_requires = \
['donphan>=3.4']

setup_kwargs = {
    'name': 'ampharos',
    'version': '2.0.1',
    'description': 'A Pokemon Database for Donphan',
    'long_description': 'Ampharos\n========\n\nLightweight Pokemon Database for use with `Donphan <https://github.com/bijij/donphan>`_ ORM.\n',
    'author': 'bijij',
    'author_email': 'josh@josh-is.gay',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
