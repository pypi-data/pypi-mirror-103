# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gareth', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.15,<4.0.0', 'PyGithub>=1.55,<2.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['gareth = gareth.gareth:main']}

setup_kwargs = {
    'name': 'gareth',
    'version': '0.1.0',
    'description': 'Tool to automate the developer setup of GrimoireLab',
    'long_description': '# gareth\n\nTool to manage the developer installation of GrimoireLab.\n\nThis software is licensed under GPL3 or later.\n\n## Requirements\n\n * Python >= 3.6\n * Poetry >= 1.0\n * Click >= 7.1.2\n * PyGithub >= 1.55\n * GitPython >= 3.1.15\n\n## Installation\n\n### Getting the source code\n\nClone the repository\n```\n$ git clone https://github.com/vchrombie/gareth/\n$ cd gareth\n```\n\n### Prerequisites\n\n#### Poetry\n\nWe use [Poetry](https://python-poetry.org/docs/) for managing the project.\nYou can install it following [these steps](https://python-poetry.org/docs/#installation).\n\nWe use [Bitergia/release-tools](https://github.com/Bitergia/release-tools) for managing \nthe releases.\n\n### Installation\n\nInstall the required dependencies (this will also create a virtual environment)\n```\n$ poetry install\n```\n\nActivate the virtual environment\n```\n$ poetry shell\n```\n\n## Usage\n\nOnce you install the tool, you can use it with the `gareth` command.\n```\n$ gareth --help\nUsage: gareth [OPTIONS]\n\n  Tool to manage the developer installation of GrimoireLab.\n\nOptions:\n  -t, --token TEXT   GitHub API Token.\n  -s, --source TEXT  The source folder of the dev env.  [default: sources]\n  --create           Create the developer setup.\n  --update           Update the developer setup.\n  --help             Show this message and exit.\n\n```\n\nCreate the developer environment setup\n```\n$ gareth -t xxxx -s sources --create\n```\n\nUpdate the developer environment setup\n```\n$ gareth -s sources --update\n```\n\n## Contributions\n\nAll the contributions are welcome. Please feel free to open an issue or a PR. \nIf you are opening any PR for the code, please be sure to add a \n[changelog](https://github.com/Bitergia/release-tools#changelog) entry.\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'Venu Vardhan Reddy Tekula',
    'author_email': 'venu@bitergia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
