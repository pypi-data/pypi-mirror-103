# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_login']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.21.1,<2.0.0',
 'python-dotenv>=0.17.0,<0.18.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tg-login = tg_login.cli:app']}

setup_kwargs = {
    'name': 'tg-login',
    'version': '0.0.1rc0',
    'description': 'A command line tool to login into Telegram with user or bot accounts.',
    'long_description': "# tg-login\n\nA command line tool to login into Telegram with user or bot accounts.\n\n## Why\n\nWhy the need of a seperate tool like `tg-login` ?\n\n## Installation\n\n```shell\npip install tg-login\n```\n\n## Usage\n\n```shell\nUsage: tg-login [OPTIONS]\n\n  A command line tool to login into Telegram with user or bot accounts.\n\nOptions:\n  -v, --version  Show version and exit.\n  --help         Show this message and exit.\n```\n\nThe `API_ID` ,`API_HASH`, `BOT_TOKEN`, `PHONE_NO`, can be passed as CLI options, or can be set as environment variables.\n\nProvide either `BOT_TOKEN` or `PHONE_NO`. If both are found, `tg-login` will use the bot account.\n\n`tg-login` by default generates the session string and saves it in your Telegram's Saved Messages.\n\nIf the `--session=file` option is provided, it will generated a session file.\n\n## Projects using `tg-login`\n\n- [tgcf](https://github.com/aahnik/tgcf)\n\nOpen a PR to add your project here!\n\n## Credits\n\nMade with Telethon.\n",
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
