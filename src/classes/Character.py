from functools import lru_cache
from pprint import pprint
from typing import Optional, Union

from discord import Embed, TextChannel

from src.classes.Item import _get_base, Item
from src.constants.ITEMS import WEAPON, HELMET, LEGS, BOOTS, COMMON


@lru_cache(maxsize=None)
def get_enemy_life(level):
    base = _get_base(level)
    return int(pow(base, 2) * 0.900900900 + level * base * 1.2012012)


class CharacterSingleton(type):
    _instances = {}

    def __call__(cls, name, *args, **kwargs):
        if name not in cls._instances:
            cls._instances[name] = \
                super(CharacterSingleton, cls).__call__(name, *args, **kwargs)

        return cls._instances[name]


class Character(metaclass=CharacterSingleton):
    """Immutable Character class"""
    _name: str
    _power: int
    _level: int
    _exp: int
    total_exp: int
    _current: bool
    _weapon: Optional[Item]
    helmet: Optional[Item]
    legs: Optional[Item]
    boots: Optional[Item]
    lock: int

    def _create_character(self, name: str, power: int, level: int, exp: int,
                          current: bool, lock: int,
                          total_exp: int = 0,
                          weapon: Optional[Item] = None,
                          helmet: Optional[Item] = None,
                          legs: Optional[Item] = None,
                          boots: Optional[Item] = None,
                          ):
        """Create a Character instance."""
        if not isinstance(name, str):
            raise ValueError("'name' must be a string")
        if not isinstance(power, int):
            raise ValueError("'power' must be a int")
        if not isinstance(level, int):
            raise ValueError("'level' must be a int")
        if not isinstance(exp, int):
            raise ValueError("'exp' must be a int")
        if not isinstance(total_exp, int):
            raise ValueError("'total_exp' must be a int")
        if not isinstance(lock, int):
            raise ValueError("'lock' must be a int")

        self._name = name
        self._power = power
        self._level = level
        self._exp = exp
        self.total_exp = total_exp
        self._current = current
        self._weapon = weapon
        self.helmet = helmet
        self.legs = legs
        self.boots = boots
        self.lock = lock

    def __init__(self, name: str = '', level: int = 1, exp: int = 0,
                 json: Optional[dict] = None):
        """Create a Item instance."""
        if json:
            total_exp = json['total_exp'] if 'total_exp' in json else 0
            weapon = Item(json=json['weapon']) if 'weapon' in json else None
            helmet = Item(json=json['helmet']) if 'helmet' in json else None
            legs = Item(json=json['legs']) if 'legs' in json else None
            boots = Item(json=json['boots']) if 'boots' in json else None
            lock = json['lock'] if 'lock' in json else 0
            self._create_character(json['name'], json['power'], json['level'],
                                   json['exp'], json['current'], lock,
                                   total_exp, weapon, helmet, legs, boots)
            return
        power = _get_base(level)
        self._create_character(name, power, level, exp, True, 0)

    def __repr__(self):
        """Create a string representation of the Character."""
        template = "<Character(name='{}', level='{}', power={})>"
        return template.format(
            self._name,
            self._level,
            self._power,
        )

    @property
    def embed(self):
        level_total_exp = \
            get_enemy_life(self._level) * 20 * (5 if self._level > 1 else 1)
        embed = Embed(title=self._name)
        embed.add_field(name='Niveau', value=str(self._level))
        embed.add_field(name='', value='')
        embed.add_field(
            name='Expérience',
            value=f'{self._exp:n}/{level_total_exp:n}'
        )
        embed.add_field(
            name='Expérience totale',
            value=f'{self.total_exp:n}'
        )
        embed.add_field(name='Puissance',
                        value=f'{self._power:n}(+{self.power - self._power:n})')
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
        return total

    def level_up(self):
        self._level += 1
        self._power = _get_base(self._level)

    def to_json(self):
        json = {
            'name': self._name,
            'current': self._current,
            'level': self._level,
            'exp': self._exp,
            'total_exp': self.total_exp,
            'power': self._power,
            'weapon': self._weapon.to_json() if self._weapon else None,
            'helmet': self.helmet.to_json() if self.helmet else None,
            'legs': self.legs.to_json() if self.legs else None,
            'boots': self.boots.to_json() if self.boots else None,
            'lock': self.lock
        }
        return json

    def gain_xp(self, xp) -> bool:
        total_xp = get_enemy_life(self._level) * 20
        if self._level > 1:
            total_xp *= 5
        self.total_exp = self.total_exp + xp
        if self._exp + xp > total_xp:
            self.level_up()
            self._exp = self._exp + xp - total_xp
            return True
        self._exp += xp
        return False


def equip_weapon(fighter, new_item):
    if fighter._weapon and fighter._weapon.power >= new_item.power:
        return False
    fighter._weapon = new_item
    return True


def equip_helmet(fighter, new_item):
    if fighter.helmet and fighter.helmet.power >= new_item.power:
        return False
    fighter.helmet = new_item
    return True


def equip_legs(fighter, new_item):
    if fighter.legs and fighter.legs.power >= new_item.power:
        return False
    fighter.legs = new_item
    return True


def equip_boots(fighter, new_item):
    if fighter.boots and fighter.boots.power >= new_item.power:
        return False
    fighter.boots = new_item
    return True


def weapon_changer(new_item):
    if new_item.type == WEAPON:
        return equip_weapon
    if new_item.type == HELMET:
        return equip_helmet
    if new_item.type == LEGS:
        return equip_legs
    if new_item.type == BOOTS:
        return equip_boots
    raise ValueError('Item type unknown')


async def get_loot(fighter: Character, channel: TextChannel):
    print('get_loot')
    new_item = Item(fighter._level)
    equip_item = weapon_changer(new_item)

    if not equip_item(fighter, new_item) or new_item.quality == COMMON \
            or not channel:
        return

    await channel.send(f'{fighter._name} vient de récupérer cet objet :',
                       embed=new_item.embed)


if __name__ == '__main__':
    print(Character('Lorel', 4))
    pprint(Character('Lorel', 42).to_json())
