# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dippy', 'dippy.core', 'dippy.core.gateway']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'gully>=0.2.0,<0.3.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'dippy.core',
    'version': '0.0.1a0',
    'description': 'Async Discord Gateway client.',
    'long_description': None,
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
