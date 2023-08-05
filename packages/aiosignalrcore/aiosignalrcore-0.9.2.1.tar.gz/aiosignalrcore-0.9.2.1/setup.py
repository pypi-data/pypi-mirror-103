# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiosignalrcore',
 'aiosignalrcore.hub',
 'aiosignalrcore.messages',
 'aiosignalrcore.messages.handshake',
 'aiosignalrcore.protocol',
 'aiosignalrcore.protocol.handshake',
 'aiosignalrcore.transport',
 'aiosignalrcore.transport.websockets']

package_data = \
{'': ['*']}

install_requires = \
['msgpack==1.0.2', 'requests>=2.22.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'aiosignalrcore',
    'version': '0.9.2.1',
    'description': 'Async fork of Python SignalR Core client(json and messagepack), with invocation auth and two way streaming. Compatible with azure / serverless functions. Also with automatic reconnect and manually reconnect.',
    'long_description': '# SignalR core client (async fork)\n[![Pypi](https://img.shields.io/pypi/v/aiosignalrcore.svg)](https://pypi.org/project/aiosignalrcore/)\n\nThis is asyncio version of the original SignalR Core [library](https://github.com/mandrewcito/signalrcore).  \nThe main difference is that `websocket` library is replaced with asyncio-compatabile `websockets`.  \nAll future changes in the original repo will be merged to this fork inheriting the major and minor version number.\n\n## Installation\n\n```\npip install aiosignalrcore\n```\n\n## Usage\n\nCheck out the [docs](https://github.com/mandrewcito/signalrcore) of the original library.  \nThe names of all modules, classes, and methods are preserved.  \n\n### Async example\n\n```python\nimport asyncio\nimport logging\nfrom aiosignalrcore.hub_connection_builder import HubConnectionBuilder\nfrom aiosignalrcore.messages.completion_message import CompletionMessage\nfrom aiosignalrcore.transport.websockets.connection import ConnectionState\n\n\nhub_connection = (\n    HubConnectionBuilder()\n        .with_url(\'%URL%\')\n        .with_automatic_reconnect(\n            {\n                "type": "raw",\n                "keep_alive_interval": 10,\n                "reconnect_interval": 5,\n                "max_attempts": 5,\n            }\n        )\n        .build()\n)\n\n\nasync def on_connect():\n    logging.info(\'Connected to the server\')\n    \n    while hub_connection.transport.state != ConnectionState.connected:\n        await asyncio.sleep(0.1)\n\n    await hub_connection.send("SendMessage", [])\n\n\nasync def on_message(message):\n    pass\n\n\ndef on_error(self, message: CompletionMessage):\n    raise Exception(message.error)\n\n\nhub_connection.on_open(on_connect)\nhub_connection.on_error(on_error)\nhub_connection.on("Message", on_message)\n\nawait hub_connection.start()\n\ntry:\n    while hub_connection.transport.state == ConnectionState.connected:\n        await asyncio.sleep(1)\nexcept KeyboardInterrupt:\n    pass\nfinally:\n    await hub_connection.stop()\n```',
    'author': 'mandrewcito',
    'author_email': 'anbaalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dipdup-net/aiosignalrcore',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
