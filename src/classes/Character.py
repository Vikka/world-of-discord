from functools import lru_cache
from json import dumps, load
from math import floor, ceil, sqrt
from os import makedirs
from os.path import isfile, dirname
from pprint import pprint
from time import time
from typing import List, Dict, Tuple
from typing import Optional
from weakref import ref

from discord import Embed, Member, Guild, TextChannel

from src.classes.Item import _get_base, Item
from src.constants import ITEMS_UTILS
from src.constants import JSON_KEY
from src.constants.CONSTANTS import LEVEL_VALUE, EXP_VALUE, POWER_VALUE, \
    KILLS_VALUE, RARES_VALUE, DUEL_VALUE
from src.constants.FIGHT import ROUND_TIME
from src.constants.ITEMS_UTILS import COMMON
from src.constants.ITEMS_UTILS import UNCOMMON, RARE
from src.constants.JSON_KEY import KILLS, LOOTS, COMMONS, UNCOMMONS, RARES, \
    PVP1V1_TOTAL_GAMES, ELO, PVP1V1_TOTAL_WIN, PVP1V1_TOTAL_LOSE
from src.constants.JSON_KEY import TOTAL_EXP, WEAPONS, ID, NAME, POWER, LEVEL, \
    LOCK, EXP, CURRENT
from src.constants.PATH import USER_PATH
from src.errors.character import NoCharacters
from src.utils.utils import clear_instances, first


@lru_cache(maxsize=None)
def get_enemy_life(level):
    switch = {
        61: 10,
        51: 9,
        41: 8,
        31: 7,
        21: 6,
        11: 5,
        0: 4,
    }
    base = _get_base(level)
    min = floor(base / 2 + level)
    min_last = base + min * switch[first(switch, lambda x: level >= x)]
    return min_last * 10


class CharacterSingleton(type):
    _instances: List[ref] = {}

    def __call__(cls, id_, *args, **kwargs):
        clear_instances(Character)
        if id_ not in cls._instances:
            instance = super(CharacterSingleton, cls).__call__(id_, *args,
                                                               **kwargs)
            weak_instance = ref(instance)
            cls._instances[id_] = weak_instance
        else:
            instance = cls._instances[id_]()
        return instance


class Character(metaclass=CharacterSingleton):
    """Immutable Character class"""
    _name: str
    id: str
    _power: int
    _level: int
    _exp: int
    _total_exp: int
    is_leader: bool
    _weapon: Optional[Item]
    helmet: Optional[Item]
    legs: Optional[Item]
    boots: Optional[Item]
    chest: Optional[Item]
    gloves: Optional[Item]
    belt: Optional[Item]
    cloak: Optional[Item]
    shoulders: Optional[Item]
    wrist: Optional[Item]
    lock: int
    _kills: int
    _loots: int
    _commons: int
    _uncommons: int
    _rares: int
    _elo: int
    pvp1v1_total_games: int

    @classmethod
    def from_json(cls, json: dict):
        total_exp = json.get(TOTAL_EXP, 0)
        weapon = Item(json=json[WEAPONS]) if json.get(WEAPONS) else None
        helmet = Item(json=json[JSON_KEY.HELMET]) \
            if JSON_KEY.HELMET in json and json[JSON_KEY.HELMET] else None
        legs = Item(json=json[JSON_KEY.LEGS]) \
            if JSON_KEY.LEGS in json and json[JSON_KEY.LEGS] else None
        boots = Item(json=json[JSON_KEY.BOOTS]) \
            if JSON_KEY.BOOTS in json and json[JSON_KEY.BOOTS] else None
        chest = Item(json=json[JSON_KEY.CHEST]) \
            if JSON_KEY.CHEST in json and json[JSON_KEY.CHEST] else None
        gloves = Item(json=json[JSON_KEY.GLOVES]) \
            if JSON_KEY.GLOVES in json and json[JSON_KEY.GLOVES] else None
        belt = Item(json=json[JSON_KEY.BELT]) \
            if JSON_KEY.BELT in json and json[JSON_KEY.BELT] else None
        cloak = Item(json=json[JSON_KEY.CLOAK]) \
            if JSON_KEY.CLOAK in json and json[JSON_KEY.CLOAK] else None
        shoulders = Item(json=json[JSON_KEY.SHOULDERS]) \
            if JSON_KEY.SHOULDERS in json and json[
            JSON_KEY.SHOULDERS] else None
        wrist = Item(json=json[JSON_KEY.WRIST]) \
            if JSON_KEY.WRIST in json and json[JSON_KEY.WRIST] else None
        lock = json[LOCK] if LOCK in json else None
        kills = json.get(KILLS, 0)
        loots = json.get(LOOTS, 0)
        commons = json.get(COMMONS, 0)
        uncommons = json.get(UNCOMMONS, 0)
        rares = json.get(RARES, 0)
        elo = json.get(ELO, 0)
        pvp1v1_total_games = json.get(PVP1V1_TOTAL_GAMES, 0)
        pvp1v1_total_lose = json.get(PVP1V1_TOTAL_LOSE, 0)
        pvp1v1_total_win = json.get(PVP1V1_TOTAL_WIN, 0)

        return cls(
            json[ID], json[NAME], json[POWER],
            json[LEVEL], json[EXP], json[CURRENT], lock, total_exp, weapon,
            helmet, legs, boots, chest, gloves, belt, cloak, shoulders, wrist,
            kills, loots, commons, uncommons, rares, elo, pvp1v1_total_games,
            pvp1v1_total_lose, pvp1v1_total_win,
        )

    def __init__(
            self, id_: str, name: str, power: Optional[int] = None,
            level: int = 1, exp: int = 0, is_leader: bool = True,
            lock: int = 0, total_exp: int = 0,
            weapon: Optional[Item] = None,
            helmet: Optional[Item] = None,
            legs: Optional[Item] = None,
            boots: Optional[Item] = None,
            chest: Optional[Item] = None,
            gloves: Optional[Item] = None,
            belt: Optional[Item] = None,
            cloak: Optional[Item] = None,
            shoulders: Optional[Item] = None,
            wrist: Optional[Item] = None,
            kills: int = 0, loots: int = 0, commons: int = 0,
            uncommons: int = 0, rares: int = 0,
            elo: int = 0,
            pvp1v1_total_games: int = 0,
            pvp1v1_total_lose: int = 0,
            pvp1v1_total_win: int = 0,
    ):
        """Create a Item instance."""
        self.id = id_
        self._name = name
        self._power = _get_base(level) if power is None else power
        self._level = level
        self._exp = exp
        self._total_exp = total_exp
        self.total_exp = total_exp
        self.is_leader = is_leader
        self._weapon = weapon
        self.helmet = helmet
        self.legs = legs
        self.boots = boots
        self.chest = chest
        self.gloves = gloves
        self.belt = belt
        self.cloak = cloak
        self.shoulders = shoulders
        self.wrist = wrist
        self._lock = lock
        self._kills = kills
        self._loots = loots
        self._commons = commons
        self._uncommons = uncommons
        self._rares = rares
        self._elo = elo
        self.pvp1v1_total_games = pvp1v1_total_games
        self.pvp1v1_total_lose = pvp1v1_total_lose
        self.pvp1v1_total_win = pvp1v1_total_win

    def __repr__(self):
        """Create a string representation of the Character."""
        template = "<Character(name='{}', level='{}', power={})>"
        return template.format(
            self._name,
            self._level,
            self._power,
        )

    def update_lock(self):
        self._lock = int(time()) + ROUND_TIME

    @property
    def lock(self):
        return self._lock

    @property
    def embed(self):
        level_total_exp = self.get_level_xp(self._level)
        embed = Embed(title=self._name)
        embed.add_field(name='Niveau', value=str(self._level))
        embed.add_field(
            name='Expérience',
            value=f'{self._exp:,}/{level_total_exp:,}'
        )
        embed.add_field(
            name='Expérience totale',
            value=f'{self._total_exp:,}'
        )
        embed.add_field(name='Puissance (niveaux + objets)',
                        value=f'{self.power:,} ({self._power:,} '
                              f'+ {self.power - self._power:,})')
        return embed

    @property
    def power(self):
        total = self._power
        if self._weapon:
            total += self._weapon.power
        if self.helmet:
            total += self.helmet.power
        if self.legs:
            total += self.legs.power
        if self.boots:
            total += self.boots.power
        if self.boots:
            total += self.boots.power
        if self.chest:
            total += self.chest.power
        if self.gloves:
            total += self.gloves.power
        if self.belt:
            total += self.belt.power
        if self.cloak:
            total += self.cloak.power
        if self.shoulders:
            total += self.shoulders.power
        return total

    @property
    def total_exp(self):
        return self._total_exp

    @total_exp.setter
    def total_exp(self, value: int):
        self._total_exp = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value

    @property
    def kills(self):
        return self._kills

    @kills.setter
    def kills(self, value: int):
        self._kills = value

    @property
    def loots(self):
        return self._loots

    @loots.setter
    def loots(self, value: int):
        self._loots = value

    def incr_loots(self):
        self._loots += 1

    @property
    def commons(self):
        return self._commons

    @commons.setter
    def commons(self, value: int):
        self._commons = value

    def incr_commons(self):
        self._commons += 1

    @property
    def uncommons(self):
        return self._uncommons

    @uncommons.setter
    def uncommons(self, value: int):
        self._uncommons = value

    def incr_uncommons(self):
        self._uncommons += 1

    @property
    def rares(self):
        return self._rares

    @rares.setter
    def rares(self, value: int):
        self._rares = value

    def incr_rares(self):
        self._rares += 1

    @property
    def pvp_power(self):
        return ceil(sqrt(sqrt(self.power))*100)

    @property
    def pvp_life(self):
        return self.pvp_power * 3

    @property
    def elo(self):
        return self._elo

    @elo.setter
    def elo(self, value):
        self._elo = value

    def incr_pvp1v1_total_games(self):
        self.pvp1v1_total_games += 1

    def incr_pvp1v1_total_lose(self):
        self.pvp1v1_total_lose += 1

    def incr_pvp1v1_total_win(self):
        self.pvp1v1_total_win += 1

    def get_value(self, key):
        switch = {
            LEVEL_VALUE: self.level,
            EXP_VALUE: self.total_exp,
            POWER_VALUE: self.power,
            KILLS_VALUE: self.kills,
            RARES_VALUE: self.rares,
            DUEL_VALUE: self.elo,
        }
        key = first(switch, lambda iterable: key in iterable)
        return switch.get(key, 0)

    def increment_stat(self, key):
        switch = {
            LOOTS: self.incr_loots,
            COMMON: self.incr_commons,
            UNCOMMON: self.incr_uncommons,
            RARE: self.incr_rares,
            PVP1V1_TOTAL_GAMES: self.incr_pvp1v1_total_games,
            PVP1V1_TOTAL_LOSE: self.incr_pvp1v1_total_lose,
            PVP1V1_TOTAL_WIN: self.incr_pvp1v1_total_win,
        }
        switch.get(first(switch, lambda x: key in x))()

    def level_up(self):
        self._level += 1
        self._power = _get_base(self._level)

    def to_json(self):
        json = {
            'name': self._name,
            'id': self.id,
            'current': self.is_leader,
            'level': self._level,
            'exp': self._exp,
            'total_exp': self._total_exp,
            'power': self._power,
            'weapons': self._weapon.to_json() if self._weapon else None,
            'helmet': self.helmet.to_json() if self.helmet else None,
            'legs': self.legs.to_json() if self.legs else None,
            'boots': self.boots.to_json() if self.boots else None,
            'chest': self.chest.to_json() if self.chest else None,
            'gloves': self.gloves.to_json() if self.gloves else None,
            'belt': self.belt.to_json() if self.belt else None,
            'cloak': self.cloak.to_json() if self.cloak else None,
            'shoulders': self.shoulders.to_json() if self.shoulders else None,
            'wrist': self.wrist.to_json() if self.wrist else None,
            'lock': self.lock,
            'kills': self._kills,
            'loots': self._loots,
            'commons': self._commons,
            'uncommons': self._uncommons,
            'rares': self._rares,
            'elo': self.elo,
            'pvp1v1_total_games': self.pvp1v1_total_games,
            'pvp1v1_total_lose': self.pvp1v1_total_lose,
            'pvp1v1_total_win': self.pvp1v1_total_win,
        }
        return json

    @staticmethod
    def get_level_xp(level: int) -> int:
        """
        :param level: The character's level.
        :return: The amount of xp required to progress to the next level.
        """
        return get_enemy_life(level) * level * 15

    def gain_xp(self, xp) -> bool:
        level_up = False
        level_xp = self.get_level_xp(self._level)
        self._total_exp += xp
        self._exp += xp
        while self._exp >= level_xp:
            self.level_up()
            self._exp -= level_xp
            level_up = True
            level_xp = self.get_level_xp(self._level)
        return level_up


def equip_weapon(fighter: Character, new_item: Item):
    if fighter._weapon and fighter._weapon.power >= new_item.power:
        return False
    fighter._weapon = new_item
    return True


def equip_helmet(fighter: Character, new_item: Item):
    if fighter.helmet and fighter.helmet.power >= new_item.power:
        return False
    fighter.helmet = new_item
    return True


def equip_legs(fighter: Character, new_item: Item):
    if fighter.legs and fighter.legs.power >= new_item.power:
        return False
    fighter.legs = new_item
    return True


def equip_boots(fighter: Character, new_item: Item):
    if fighter.boots and fighter.boots.power >= new_item.power:
        return False
    fighter.boots = new_item
    return True


def equip_chest(fighter: Character, new_item: Item):
    if fighter.chest and fighter.chest.power >= new_item.power:
        return False
    fighter.chest = new_item
    return True


def equip_gloves(fighter: Character, new_item: Item):
    if fighter.gloves and fighter.gloves.power >= new_item.power:
        return False
    fighter.gloves = new_item
    return True


def equip_belt(fighter: Character, new_item: Item):
    if fighter.belt and fighter.belt.power >= new_item.power:
        return False
    fighter.belt = new_item
    return True


def equip_cloak(fighter: Character, new_item: Item):
    if fighter.cloak and fighter.cloak.power >= new_item.power:
        return False
    fighter.cloak = new_item
    return True


def equip_shoulders(fighter: Character, new_item: Item):
    if fighter.shoulders and fighter.shoulders.power >= new_item.power:
        return False
    fighter.shoulders = new_item
    return True


def equip_wrist(fighter: Character, new_item: Item):
    if fighter.wrist and fighter.wrist.power >= new_item.power:
        return False
    fighter.wrist = new_item
    return True


def weapon_changer(new_item):
    switch = {
        ITEMS_UTILS.BOW: equip_weapon,
        ITEMS_UTILS.DAGGER: equip_weapon,
        ITEMS_UTILS.MACE: equip_weapon,
        ITEMS_UTILS.SWORD: equip_weapon,
        ITEMS_UTILS.HELMET: equip_helmet,
        ITEMS_UTILS.LEGS: equip_legs,
        ITEMS_UTILS.BOOTS: equip_boots,
        ITEMS_UTILS.CHEST: equip_chest,
        ITEMS_UTILS.GLOVES: equip_gloves,
        ITEMS_UTILS.BELT: equip_belt,
        ITEMS_UTILS.CLOAK: equip_cloak,
        ITEMS_UTILS.SHOULDERS: equip_shoulders,
        ITEMS_UTILS.WRIST: equip_wrist,
    }
    if new_item.type in switch:
        return switch.get(new_item.type)
    raise ValueError('Item type unknown')


def get_loot(fighter: Character, channel: TextChannel):
    print('get_loot')
    new_item = Item(fighter._level)
    equip_item = weapon_changer(new_item)

    fighter.increment_stat(new_item.quality)
    fighter.increment_stat(LOOTS)

    if not equip_item(fighter, new_item) \
            or new_item.quality in [COMMON, UNCOMMON] \
            or not channel:
        return
    return f'{fighter._name} vient de récupérer cet objet :', new_item.embed


def _get_character(path: str) -> Dict[str, Character]:
    content = {}
    if isfile(path):
        with open(path) as new_file:
            content = load(new_file)
    if not content:
        return {}
    return {id_: Character.from_json(character) for id_, character in
            content.items()}


def get_leader(characters: Dict[str, Character]) -> Optional[Character]:
    if not characters:
        raise NoCharacters

    for name, character in characters.items():
        if character.is_leader:
            return character


def get_path_and_characters(author: Member, guild: Guild) \
        -> Tuple[str, Dict[str, Character]]:
    file_name = f'{author.id}-{guild.id}.json'
    path = USER_PATH.format(guild.id, file_name)
    characters = _get_character(path)
    return path, characters


def store_characters(path: str, characters_list: Dict[str, Character]):
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


def leader_from_author_guild(author, guild):
    _, characters = get_path_and_characters(author, guild)
    return get_leader(characters)


if __name__ == '__main__':
    print(Character('Lorel', 4))
    pprint(Character('Lorel', 42).to_json())
