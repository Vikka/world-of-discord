from typing import List

from src.commands.character import Personnage


class Guild:
    id: int

    def __init__(self, id_: int):
        self.id = id_


class Member:
    id: int

    def __init__(self, id_: int):
        self.id = id_


class Context:
    guild: Guild
    author: Member
    send_res: List[str]

    def __init__(self, guild: Guild, author: Member):
        self.guild = guild
        self.author = author
        self.send_res = list()

    def send(self, x):
        self.send_res.append(x)


def test_create(monkeypatch):
    from src.manipulation import character_manipulation
    def _get_character(_):
        return {}

    def store_characters(_, __):
        ...

    monkeypatch.setattr(character_manipulation, '_get_character',
                        _get_character)
    monkeypatch.setattr(character_manipulation, 'store_characters',
                        store_characters)
    guild = Guild(1)
    author = Member(2)
    ctx = Context(guild, author)
    await Personnage.create('Spam')

