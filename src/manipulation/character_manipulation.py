from json import dumps, load
from os import makedirs
from os.path import isfile, dirname
from typing import Dict

from discord import Member, Guild

from src.errors.character import NoCharacters
from src.constants.PATH import USER_PATH

from src.classes.Character import Character


def _get_character(path: str) -> Dict[str, Character]:
    content = {}
    if isfile(path):
        with open(path) as new_file:
            content = load(new_file)
    if not content:
        return {}
    return {id_: Character(id_, json=character) for id_, character in
            content.items()}


def get_leader(characters):
    if not characters:
        raise NoCharacters

    for name, character in characters.items():
        if character.is_leader:
            return character


def get_path_and_characters(author: Member, guild: Guild):
    file_name = f'{author.id}-{guild.id}.json'
    path = USER_PATH.format(guild.id, file_name)
    characters = _get_character(path)
    return path, characters


def _store_characters(path: str, characters_list: Dict[str, Character]):
    makedirs(dirname(path), exist_ok=True)
    if isfile(path):
        with open(path, 'w') as new_file:
            new_file.write(
                dumps({id_: character.to_json() for id_, character in
                       characters_list.items()})
            )
    else:
        with open(path, 'x') as new_file:
            new_file.write(
                dumps({id_: character.to_json() for id_, character in
                       characters_list.items()})
            )
