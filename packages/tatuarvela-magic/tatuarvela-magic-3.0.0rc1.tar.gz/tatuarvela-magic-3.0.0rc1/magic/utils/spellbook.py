import json
import os

from fastjsonschema import validate

from magic.config import SPELLBOOK_INDENTATION, SPELLBOOK_PATH, SPELLBOOK_SCHEMA_PATH

default_spell = {
    "description": "Test echo spell with arguments '$a0' and '$a1'",
    "magicWords": ["t", "test"],
    "commands": ["echo $a0", "echo $a1"],
    "argumentCount": 2,
}


def __create_spellbook():
    with open(SPELLBOOK_PATH, "x") as file:
        json.dump([default_spell], file, indent=SPELLBOOK_INDENTATION)


def __validate_spellbook(spellbook_contents):
    try:
        with open(SPELLBOOK_SCHEMA_PATH, "r") as file:
            schema = json.load(file)
            validate(schema, spellbook_contents)
    except Exception as error:
        raise Exception(f"Spellbook is invalid: {error}")


def __open_spellbook():
    if not os.path.exists(SPELLBOOK_PATH):
        __create_spellbook()
    with open(SPELLBOOK_PATH, "r") as file:
        spellbook = json.load(file)
        __validate_spellbook(spellbook)
        return spellbook


def get_spells():
    spellbook = __open_spellbook()
    spells = dict()
    for entry in spellbook:
        for magic_word in entry["magicWords"]:
            if spells.get(magic_word):
                raise Exception(f"Spellbook has duplicated magic word: {magic_word}")
            spells[magic_word] = entry
    return spells


def get(magic_word):
    spells = get_spells()
    return spells.get(magic_word)


def write(spell):
    with open(SPELLBOOK_PATH, "r+") as file:
        spellbook = json.load(file)  # spells are already validated in add_spell()
        spellbook.append(spell)
        file.seek(0)
        json.dump(spellbook, file, indent=SPELLBOOK_INDENTATION)
        file.truncate()


def delete(magic_word):
    with open(SPELLBOOK_PATH, "r+") as file:

        def magic_word_filter(spell):
            if magic_word in spell["magicWords"]:
                return False
            else:
                return True

        spellbook = json.load(file)  # spell validity does not matter here
        spellbook = list(filter(magic_word_filter, spellbook))
        file.seek(0)
        json.dump(spellbook, file, indent=SPELLBOOK_INDENTATION)
        file.truncate()
