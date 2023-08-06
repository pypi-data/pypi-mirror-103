from magic.show import show_spell
from magic.utils.display import Colors, Emoji
from magic.utils.prompt import create_prompt
from magic.utils.spellbook import delete
from magic.utils.validate import is_y_or_n

color = Colors.YELLOW
prompt = create_prompt(color)


def delete_spell(magic_word):
    show_spell(magic_word, spell_args=[])
    confirm = prompt(
        f"{Emoji.TRASH} Do you want to delete this spell, y or n?",
        validate=is_y_or_n,
        default="n",
    )

    if confirm == "y":
        delete(magic_word)
