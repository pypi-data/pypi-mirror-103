# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dippy', 'dippy.core', 'dippy.core.gateway']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'gully>=0.2.3,<0.3.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'dippy.core',
    'version': '0.0.1a1',
    'description': 'Async Discord Gateway client.',
    'long_description': '# Dippy.Core\n\nThis is a bare-bones Discord gateway client that can be used to build Python bot frameworks for Discord. \n\n## Installation\n```shell\npip install dippy.core\n```\n\n## Usage\n\n### Connecting\n```python\nfrom dippy.core import GatewayConnection, Intents\nfrom asyncio import get_event_loop\n\nclient = GatewayConnection("YOUR.TOKEN.HERE", intents=Intents.DEFAULT | Intents.MEMBERS)\n\nloop = get_event_loop()\nloop.create_task(client.connect())\nloop.run_forever()\n```\n\n### Watching For Events\n```python\nasync def on_ready(event_payload):\n    print(event_payload.data)\n\nclient.on(on_ready, "READY")\n```\n\n## Future\n\n- Add models to wrap the event payload data\n- Add a caching interface\n- Add rate limiting\n- Add methods to models for using the gateway\n',
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZechCodes/dippy.core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
