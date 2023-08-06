from magic.utils.display import Colors, in_color
from magic.utils.spellbook import get


def show_spell(magic_word, spell_args):
    spell = get(magic_word)
    color = Colors.MAGENTA

    if not spell:
        raise Exception(f"Spell not found for magic word: {magic_word}")

    print(f'{in_color("Description:", color)} {spell["description"]}')
    print(f'{in_color("Magic words:", color)} {", ".join(spell["magicWords"])}')
    print(in_color("Commands:", color))
    for command in spell["commands"]:
        print(f"{command}")

    argument_count = spell.get("argumentCount")
    if argument_count is None:
        print(f'{in_color("Arguments required:", color)} None')
    else:
        arg_color = Colors.GREEN if len(spell_args) == argument_count else Colors.RED
        print(
            f'{in_color("Arguments required:", color)} {in_color(argument_count, arg_color)}'
        )

    if len(spell_args) > 0:
        print(in_color("Arguments provided:", color))
        for idx, arg in enumerate(spell_args):
            print(f"  {idx}: {arg}")
