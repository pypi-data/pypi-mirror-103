# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evernote_backup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'evernote3>=1.25.14,<2.0.0',
 'oauth2>=1.9.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['evernote-backup = evernote_backup.cli:main']}

setup_kwargs = {
    'name': 'evernote-backup',
    'version': '1.2.0',
    'description': 'Backup & export Evernote notes and notebooks.',
    'long_description': "# evernote-backup\n\n[![PyPI version](https://img.shields.io/pypi/v/evernote-backup?label=version)](https://pypi.python.org/pypi/evernote-backup)\n[![Python Version](https://img.shields.io/pypi/pyversions/evernote-backup.svg)](https://pypi.org/project/evernote-backup/)\n[![tests](https://github.com/vzhd1701/evernote-backup/actions/workflows/test.yml/badge.svg)](https://github.com/vzhd1701/evernote-backup/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/vzhd1701/evernote-backup/branch/master/graph/badge.svg)](https://codecov.io/gh/vzhd1701/evernote-backup)\n\nBackup your notes & notebooks from Evernote locally and export them at any time!\n\n## Features\n\n- Quickly sync all your notes into the SQLite database for backup.\n- Export all backed up notes in `*.enex` format, as **notebooks** or **single notes**.\n\n## Installation\n\n```bash\n$ pip install evernote-backup\n```\n\nOr, since **evernote-backup** is a standalone tool, it might be more convenient to install it using [**pipx**](https://github.com/pipxproject/pipx):\n\n```bash\n$ pipx install evernote-backup\n```\n\n## Usage\n\n### Step 1. Database initialization\n\nTo start you need to initialize your database.\n\n```console\n$ evernote-backup init-db\nUsername or Email: user@example.com\nPassword:\nLogging in to Evernote...\nEnter one-time code: 120917\nAuthorizing auth token, evernote backend...\nSuccessfully authenticated as user!\nCurrent login will expire at 2022-03-10 10:22:00.\nInitializing database en_backup.db...\nReading database en_backup.db...\nSuccessfully initialized database for user!\n```\n\nBy default, it will prompt you to enter your account credentials. You can provide them beforehand with `--user` and `--password` options.\n\nIf you log in to Evernote with Google or Apple accounts, you must use the `--oauth` option.\n\nTo connect to **Yinxiang** instead of Evernote, use `--backend china` option. Unfortunately, OAuth is not supported for **Yinxiang** yet.\n\n### Step 2. Downloading Evernote data\n\nThen you will be able to sync your account data.\n\n```console\n$ evernote-backup sync\nReading database en_backup.db...\nAuthorizing auth token, evernote backend...\nSuccessfully authenticated as user!\nCurrent login will expire at 2022-03-10 10:22:00.\nSyncing latest changes...\n  [####################################]  6763/6763\n566 notes to download...\n  [####################################]  566/566\nUpdated or added notebooks: 23\nUpdated or added notes: 566\nExpunged notebooks: 0\nExpunged notes: 0\nSynchronization completed!\n```\n\nYou can interrupt this process at any point. It will continue from where it's left off when you will rerun `evernote-backup sync`.\n\n**evernote-backup** keeps track of the sync state and downloads only new changes that have been made since the last run. So every sync will go pretty fast, but you'll have to wait for a bit on the first run if you have a lot of notes in your account.\n\n### Step 3. Exporting `*.enex` files\n\nFinally, you can export your data into specified **output directory**\n\n```console\n$ evernote-backup export output_dir/\nReading database en_backup.db...\nExporting notes...\n  [####################################]  23/23\nAll notes have been exported!\n```\n\nBy default, **evernote-backup** will export notes by packing them into notebooks, one `*.enex` file each. If you want to extract notes as **separate files**, use the `--single-notes` flag.\n\nTo also include **trashed** notes in export, use the `--include-trash` flag.\n\nThat's it! So to export all your Evernote data, you will have to run three commands:\n\n```console\n$ evernote-backup init-db\n$ evernote-backup sync\n$ evernote-backup export output_dir/\n```\n\nAfter first initialization, you can schedule `evernote-backup sync` command to keep your local database always up-to-date.\n\n### How to refresh expired token\n\nIn case your auth token that you initialized your database with expires, you have an option to re-authorize it by running the `evernote-backup reauth` command. It has the same options as the `init-db` command.\n\n## Dependencies\n\n- `evernote3` - to access Evernote API\n- `oauth2` - to perform OAuth authentication\n- `xmltodict` - to convert Evernote internal representation of notes into XML\n- `click` - to create a CLI interface\n",
    'author': 'vzhd1701',
    'author_email': 'vzhd1701@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vzhd1701/evernote-backup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
