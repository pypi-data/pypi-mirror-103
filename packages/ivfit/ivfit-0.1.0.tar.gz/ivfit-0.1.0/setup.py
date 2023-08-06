# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ivfit']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.3.1,<3.0.0', 'lmfit>=1.0.2,<2.0.0', 'panel>=0.11.3,<0.12.0']

setup_kwargs = {
    'name': 'ivfit',
    'version': '0.1.0',
    'description': 'Interactive, visual, fitting toolkit',
    'long_description': None,
    'author': 'Jonathan Okasinski',
    'author_email': 'jonathan.okasinski@gmail.com',
    'maintainer': 'Jonathan Okasinski',
    'maintainer_email': 'jonathan.okasinski@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
