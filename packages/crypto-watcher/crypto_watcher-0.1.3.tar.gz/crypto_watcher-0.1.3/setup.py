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
    'version': '0.1.3',
    'description': 'Monitoring for binance and NBMiner.',
    'long_description': '# Crypto watcher\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crypto_watcher?style=for-the-badge)](https://pypi.org/project/crypto-watcher/)\n[![PyPI](https://img.shields.io/pypi/v/crypto_watcher?style=for-the-badge)](https://pypi.org/project/crypto-watcher/)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/crypto_watcher/Release%20crypto_watcher?style=for-the-badge)\n\n\n## Cryptocurrency monitoring made simple.\n\nThis tool integrates with Binance, NBMiner and Cryptonator.\n\nIt\' really simple to use. It monitors your crypto-currency minerson binance and shows your current profits converted to your local currency! Isn\'t that great?\n\nYou can take a look how it looks like.\n\n[![asciicast](https://asciinema.org/a/409013.svg)](https://asciinema.org/a/409013?autoplay=1)\n\n## Installation\n\nTo install the crypto_watcher you only need Python and Pip installed. And now you need to do the following:\n```bash\npip install "crypto_watcher"\n```\n\nAnd now you can run it.\n\n## Usage\n\nYou need to create and place somewhere your secrets file. It\'s  just a JSON file.\n```json\n{\n    "api_key": "<your api key from binance>",\n    "secret_key": "<your secret key from binance>",\n    "user_name": "<your username>", // Your binance mining account username.\n    "algorithm": "ethash" // This algorithm is used, if watcher can\'t connect to NBMiner API.\n}\n```\nDefault location of secrets file is `~/.binance_secrets`. But you can set your own by providing a parameter.\n\nIf you want to watch from other machine than your miner, you need to provide custom `--nbminer_api` parameter.\n\nUsage:\n```\ncrypto_watcher -n "http://192.168.1.55:22333/" -c EUR\n```\n\nAlso, if binance can\'t handle your queries you can switch between binance api urls. You can find additional adresses [here](https://binance-docs.github.io/apidocs/spot/en/#general-info).\n\nYou can always check the `--help`.\n',
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
