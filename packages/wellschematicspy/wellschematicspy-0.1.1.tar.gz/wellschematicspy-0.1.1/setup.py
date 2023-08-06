# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wellschematicspy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.1,<4.0.0', 'numpy>=1.20.2,<2.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'wellschematicspy',
    'version': '0.1.1',
    'description': 'Oil&Gas Well Schematics definition and plot',
    'long_description': None,
    'author': 'Santiago Cuervo',
    'author_email': 'scuervo91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
