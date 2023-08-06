# ![Magic icon](./icon.png?raw=true "Magic icon") Magic

[![Repository](https://img.shields.io/badge/repository-gray.svg?logo=github)](https://github.com/TatuArvela/Magic)
[![GitHub issues](https://img.shields.io/github/issues/TatuArvela/Magic)](https://github.com/TatuArvela/Magic/issues)
[![Pipeline status](https://github.com/TatuArvela/Magic/actions/workflows/verify.yml/badge.svg?event=push)](https://github.com/TatuArvela/Magic/actions/workflows/verify.yml)
![PyPI](https://img.shields.io/pypi/v/tatuarvela-magic)
[![License](https://img.shields.io/github/license/TatuArvela/Magic)](https://github.com/TatuArvela/Magic/blob/master/LICENSE)
[![Created at Nitor](https://img.shields.io/badge/created%20at-Nitor-informational.svg)](https://nitor.com/)

Magic is a tool for wrapping repeated command line tasks into simple
scripts.

* A set of commands is saved as a **spell**
* Spells are written into the **spellbook** file (`~/.spellbook.json`)
* Each spell can be called with one or several **magic words**  
  e.g. `magic build-app` and `magic ba`
* Spells can have **arguments** passed to them  
  e.g. `magic say abra kadabra`
* The execution time of spells is reported by default

## Installation

Magic is designed for macOS and common Linux
distributions using Bash or Zsh. Windows is not supported.

Magic requires Python 3.9, and can be installed using pip:  
```console
python3 -m pip install tatuarvela-magic
```

See also: [Development installation](#development-installation)

## Usage

```console
$ magic --help
✨ Magic v3.0.0, © 2021 Tatu Arvela
A tool for simplifying repeated command line tasks

Usage:
    magic [-s | --show] <spell> [<args>...]
    magic [-d | --delete] <spell>
    magic -a | --add
    magic -e | --edit
    magic -l | --list
    magic -h | --help
    magic -v | --version

Options:
    -s --show       show spell details
    -d --delete     delete spell from spellbook
    -a --add        add spell to spellbook
    -e --edit       edit spellbook
    -l --list       list spells in spellbook
    -h --help       show help
    -v --version    show version
```

Editing a spell is currently done with an external editor (**Visual Studio
Code** by default).

### Spell arguments

Spells can have an array of arguments, which are populated according to their
index. Excessive usage is considered an anti-pattern.

Example:

```json
{
  "description": "Test echo spell with arguments '$a0' and '$a1'",
  "magicWords": [
    "t",
    "test"
  ],
  "commands": [
    "echo $a0",
    "echo $a1"
  ],
  "argumentCount": 2
}
```

```console
$ magic test cat dog
✨ Test echo spell with arguments 'cat' and 'dog'
cat
dog
✅ 23:46:43 | ⏱ 0:00:00
```

#### Advanced usage: Empty arguments

Argument are handled as an array, so arguments can not be empty. As a
work-around they may be substituted with an empty string: `''`.

#### Advanced usage: Spell options

It is possible to provide options (`--option`) as arguments to spells. This is
not intended usage, but may be useful to some. This requires a little
work-around, as `docopt` stops the execution if it detects unknown options. You
can provide the options your spell requires by adding a space and
quotes `' --option'`.

## Development

### Development installation

* Supported operating systems: macOS (untested on Linux)
* Requirements: Python 3, Poetry

1. Clone the Git repository somewhere and navigate to it on the command line

   ```bash
   git clone https://github.com/TatuArvela/Magic.git
   cd Magic
   ```

2. Install `magic` and its dependencies to a virtual env

   ```bash
   poetry install
   ```

3. Verify that `magic` works

   ```bash
   poetry run magic
   ```

4. Register `magic` to your `PATH`

    ```bash
    python -m write_path
    ```

When developing the tool, you should use the `magic` module directly
with `python -m magic`.

After successful changes, you need to run `poetry install` again to update the
version in your `PATH`.

### Code quality tools

Magic uses `isort`, `black` and `flake8` as its code quality tools. They are
executed automatically with `pre-commit` and can also be executed with the
included lint script:

```bash
python -m lint
```

### TODO

#### For 3.X.X releases

* Add `pytest`, `coverage.py`
* Replace `docopt` with `click`
  * https://click.palletsprojects.com/en/7.x/
