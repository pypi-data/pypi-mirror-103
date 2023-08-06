import re

from magic.utils.display import Colors, Emoji, in_color
from magic.utils.prompt import create_prompt
from magic.utils.spellbook import write
from magic.utils.validate import is_not_empty, is_y_or_n, magic_word_validator

color = Colors.CYAN
prompt = create_prompt(color)
multiline_prompt = create_prompt(color, multiline=True)
step_index = 0


def __step():
    global step_index
    step_index += 1
    return step_index


def __count_arguments(description, commands):
    arg_matcher = "\\$a[0-9]+"

    combined_strings = f"{description} {' '.join(commands)}"
    args = re.findall(arg_matcher, combined_strings)
    for index, arg in enumerate(args):
        args[index] = int(arg.replace("$a", ""))
    args.sort()

    if len(args) == 0:
        return 0
    return args[-1] + 1


def add_spell():
    print(in_color(f"{Emoji.WIZARD} Adding a new spell to your spellbook", color))

    description = prompt(
        f"{__step()}. Enter a description. You may use $a0, $a1, etc. to be shown as part of the message.",
        validate=is_not_empty,
    )

    magic_words = prompt(
        f"{__step()}. Enter magic words, separated by a comma:",
        validate=magic_word_validator(),
    )
    magic_words = [word.strip(" ") for word in magic_words.split(",")]

    commands = multiline_prompt(
        f"{__step()}. Enter commands to be run in the spell, separated by line breaks. "
        f"You may use $a0, $a1, etc. to provide arguments. Leave an empty line to stop."
    )

    show_message = prompt(
        f"{__step()}. Show message when casting the spell, y or n?",
        validate=is_y_or_n,
        default="y",
    )
    show_message = show_message == "y"

    show_success_message = prompt(
        f"{__step()}. Show success message, y or n?", validate=is_y_or_n, default="y"
    )
    show_success_message = show_success_message == "y"

    spell = {
        "description": description,
        "magicWords": magic_words,
        "commands": commands,
        "argumentCount": __count_arguments(description, commands),
        "showMessage": show_message,
        "showSuccessMessage": show_success_message,
    }

    write(spell)
