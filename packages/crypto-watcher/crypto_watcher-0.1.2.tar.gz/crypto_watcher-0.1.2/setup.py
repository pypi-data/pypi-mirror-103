# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crypto_watcher',
 'crypto_watcher.services.binance',
 'crypto_watcher.services.cryptonator',
 'crypto_watcher.services.nbminer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0', 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['crypto_watcher = crypto_watcher.main:main']}

setup_kwargs = {
    'name': 'crypto-watcher',
    'version': '0.1.2',
    'description': 'Monitoring for binance and NBMiner.',
    'long_description': '# Crypto watcher\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crypto_watcher?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/crypto_watcher?style=for-the-badge)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/crypto_watcher/Release%20crypto_watcher?style=for-the-badge)\n\n\nSimple monitoring for your crypto miner.\n\nThis tool integrates with binance and NBMiner.\n\nAdd secrets file before use.\n```\n{\n    "api_key": "<your api key from binance>",\n    "secret_key": "<your secret key from binance>",\n    "user_name": "<your username>",\n    "algorithm": "ethash"\n}\n```\nDefault location of secrets file is `~/.binance_secrets`. But you can set your own by providing parameter.\n\nIf you watching from other machine than your miner. You need to provide custom `--nbminer_api` parameter.\n\nUsage:\n```\ncrypto_watcher -n "http://192.168.1.55:22333/" -c EUR\n```\n\nYou can always check the `--help`.\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/crypto_watcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
