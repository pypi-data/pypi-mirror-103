"""A tool for simplifying repeated command line tasks

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
    -v --version    show version"""
import subprocess  # nosec
from datetime import datetime, timedelta
from importlib import metadata
from sys import exit

from docopt import docopt

from magic.add import add_spell
from magic.cast import cast_spell
from magic.config import SPELLBOOK_EDITOR, SPELLBOOK_PATH
from magic.delete import delete_spell
from magic.list import list_spells
from magic.show import show_spell
from magic.utils.display import Colors, Emoji, in_color, print_error

__version__ = metadata.version("tatuarvela-magic")
VERSION_STRING = f'{Emoji.SPARKLE} {in_color("Magic", Colors.BLUE)} v{__version__}, © 2021 Tatu Arvela'
DOC_STRING = f"{VERSION_STRING}\n{__doc__}"


def main():
    arguments = docopt(DOC_STRING, version=VERSION_STRING)

    show_arg = arguments["--show"]
    delete_arg = arguments["--delete"]
    add_arg = arguments["--add"]
    edit_arg = arguments["--edit"]
    list_arg = arguments["--list"]
    magic_word = arguments["<spell>"]
    spell_args = arguments["<args>"]

    try:
        if show_arg is True:
            show_spell(magic_word=magic_word, spell_args=spell_args)
            exit()

        if delete_arg is True:
            delete_spell(magic_word=magic_word)
            exit()

        if add_arg is True:
            add_spell()
            exit()

        if edit_arg is True:
            # TODO: custom editor with validation
            subprocess.call([SPELLBOOK_EDITOR, SPELLBOOK_PATH])  # nosec
            exit()

        if list_arg is True:
            list_spells()
            exit()

    except Exception as error:
        print_error(error)
        exit()

    handle_spell_cast(arguments)


def handle_spell_cast(arguments):
    start_time = datetime.now()

    try:
        show_success_message = cast_spell(arguments)
        if show_success_message:
            print_result(start_time, success=True)

    except RuntimeError:
        print_result(start_time, success=False)


def print_result(start_time, success):
    current_time = datetime.now().strftime("%H:%M:%S")
    elapsed_time = datetime.now() - start_time
    elapsed_time = elapsed_time - timedelta(microseconds=elapsed_time.microseconds)

    result_emoji = Emoji.SUCCESS if success else Emoji.FAILURE
    time_message = (
        in_color(current_time, Colors.GREEN)
        if success
        else in_color(current_time, Colors.RED)
    )

    print(f"{result_emoji} {time_message} | {Emoji.TIMER} {elapsed_time}")
