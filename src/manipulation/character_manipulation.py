from json import dumps, load
from os.path import isfile
from typing import Dict

from discord import Member, Guild

from src.classes.Character import Character
from src.constants.PATH import USER_PATH


def _get_character(path: str) -> Dict[str, Character]:
    content = {}
    if isfile(path):
        with open(path) as new_file:
            content = load(new_file)
    if not content:
        return {}
    return {name: Character(name, json=character) for name, character in
            content.items()}


def get_leader(characters):
    if not characters:
        return

    for name, character in characters.items():
        if character._current:
            return character


def _get_path_and_characters(author: Member, guild: Guild):
    file_name = f'{author.id}-{guild.id}.json'
    path = USER_PATH.format(file_name)
    characters = _get_character(path)
    return path, characters


def _store_characters(path: str, characters_list: Dict[str, Character]):
    if isfile(path):
        with open(path, 'w') as new_file:
            new_file.write(
                dumps({name: character.to_json() for name, character in
                       characters_list.items()})
            )
    else:
        with open(path, 'x') as new_file:
            new_file.write(
                dumps({name: character.to_json() for name, character in
                       characters_list.items()})
                )
