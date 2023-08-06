# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic', 'magic.utils']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'fastjsonschema>=2.15.0,<3.0.0']

entry_points = \
{'console_scripts': ['magic = magic:main']}

setup_kwargs = {
    'name': 'tatuarvela-magic',
    'version': '3.0.0rc1',
    'description': 'A tool for simplifying repeated command line tasks',
    'long_description': '# ![Magic icon](./icon.png?raw=true "Magic icon") Magic\n\n[![Repository](https://img.shields.io/badge/repository-gray.svg?logo=github)](https://github.com/TatuArvela/Magic)\n[![GitHub issues](https://img.shields.io/github/issues/TatuArvela/Magic)](https://github.com/TatuArvela/Magic/issues)\n[![Pipeline status](https://github.com/TatuArvela/Magic/actions/workflows/verify.yml/badge.svg?event=push)](https://github.com/TatuArvela/Magic/actions/workflows/verify.yml)\n![PyPI](https://img.shields.io/pypi/v/tatuarvela-magic)\n[![License](https://img.shields.io/github/license/TatuArvela/Magic)](https://github.com/TatuArvela/Magic/blob/master/LICENSE)\n[![Created at Nitor](https://img.shields.io/badge/created%20at-Nitor-informational.svg)](https://nitor.com/)\n\nMagic is a tool for wrapping repeated command line tasks into simple\nscripts.\n\n* A set of commands is saved as a **spell**\n* Spells are written into the **spellbook** file (`~/.spellbook.json`)\n* Each spell can be called with one or several **magic words**  \n  e.g. `magic build-app` and `magic ba`\n* Spells can have **arguments** passed to them  \n  e.g. `magic say abra kadabra`\n* The execution time of spells is reported by default\n\n## Installation\n\nMagic is designed for macOS and common Linux\ndistributions using Bash or Zsh. Windows is not supported.\n\nMagic requires Python 3.9, and can be installed using pip:  \n```console\npython3 -m pip install tatuarvela-magic\n```\n\nSee also: [Development installation](#development-installation)\n\n## Usage\n\n```console\n$ magic --help\n✨ Magic v3.0.0, © 2021 Tatu Arvela\nA tool for simplifying repeated command line tasks\n\nUsage:\n    magic [-s | --show] <spell> [<args>...]\n    magic [-d | --delete] <spell>\n    magic -a | --add\n    magic -e | --edit\n    magic -l | --list\n    magic -h | --help\n    magic -v | --version\n\nOptions:\n    -s --show       show spell details\n    -d --delete     delete spell from spellbook\n    -a --add        add spell to spellbook\n    -e --edit       edit spellbook\n    -l --list       list spells in spellbook\n    -h --help       show help\n    -v --version    show version\n```\n\nEditing a spell is currently done with an external editor (**Visual Studio\nCode** by default).\n\n### Spell arguments\n\nSpells can have an array of arguments, which are populated according to their\nindex. Excessive usage is considered an anti-pattern.\n\nExample:\n\n```json\n{\n  "description": "Test echo spell with arguments \'$a0\' and \'$a1\'",\n  "magicWords": [\n    "t",\n    "test"\n  ],\n  "commands": [\n    "echo $a0",\n    "echo $a1"\n  ],\n  "argumentCount": 2\n}\n```\n\n```console\n$ magic test cat dog\n✨ Test echo spell with arguments \'cat\' and \'dog\'\ncat\ndog\n✅ 23:46:43 | ⏱ 0:00:00\n```\n\n#### Advanced usage: Empty arguments\n\nArgument are handled as an array, so arguments can not be empty. As a\nwork-around they may be substituted with an empty string: `\'\'`.\n\n#### Advanced usage: Spell options\n\nIt is possible to provide options (`--option`) as arguments to spells. This is\nnot intended usage, but may be useful to some. This requires a little\nwork-around, as `docopt` stops the execution if it detects unknown options. You\ncan provide the options your spell requires by adding a space and\nquotes `\' --option\'`.\n\n## Development\n\n### Development installation\n\n* Supported operating systems: macOS (untested on Linux)\n* Requirements: Python 3, Poetry\n\n1. Clone the Git repository somewhere and navigate to it on the command line\n\n   ```bash\n   git clone https://github.com/TatuArvela/Magic.git\n   cd Magic\n   ```\n\n2. Install `magic` and its dependencies to a virtual env\n\n   ```bash\n   poetry install\n   ```\n\n3. Verify that `magic` works\n\n   ```bash\n   poetry run magic\n   ```\n\n4. Register `magic` to your `PATH`\n\n    ```bash\n    python -m write_path\n    ```\n\nWhen developing the tool, you should use the `magic` module directly\nwith `python -m magic`.\n\nAfter successful changes, you need to run `poetry install` again to update the\nversion in your `PATH`.\n\n### Code quality tools\n\nMagic uses `isort`, `black` and `flake8` as its code quality tools. They are\nexecuted automatically with `pre-commit` and can also be executed with the\nincluded lint script:\n\n```bash\npython -m lint\n```\n\n### TODO\n\n#### For 3.X.X releases\n\n* Add `pytest`, `coverage.py`\n* Replace `docopt` with `click`\n  * https://click.palletsprojects.com/en/7.x/\n',
    'author': 'Tatu Arvela',
    'author_email': 'tatu.arvela@nitor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TatuArvela/Magic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
