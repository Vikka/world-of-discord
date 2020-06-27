from collections import defaultdict
from functools import lru_cache
from locale import setlocale, LC_ALL
from pprint import pprint
from random import choices, randint, choice
from typing import Literal, Optional

from discord import Embed

from src.constants.CONSTANTS import STAT_BASE
from src.constants.ITEMS_UTILS import RARITY_PROB, COMMON, UNCOMMON, RARE, TYPES, COLOR, \
    WEAPON, WEAPON_TYPES
from src.constants.PATH import IMG_LINKS_PATH, ITEM_NAME_PATH, \
    RARE_ITEM_NAME_PATH

setlocale(LC_ALL, '')

with open(IMG_LINKS_PATH, encoding='utf-8') as img_links_folder:
    IMG_LINKS = img_links_folder.read().splitlines()


def _get_rarity(rarity):
    if rarity:
        return RARITY_PROB[rarity][0]
    final_rarity = choices([name[0] for name in RARITY_PROB],
                           cum_weights=[name[1] for name in RARITY_PROB])[0]
    return final_rarity


@lru_cache(maxsize=None)
def _get_base(level: int, stat: int = STAT_BASE + 1):
    return int(1.1 * _get_base(level - 1) if level - 1 else stat)


@lru_cache(maxsize=None)
def _common_stat(base, level):
    common_min = int(base / 2 + level)
    common_max = int(common_min + base / 5)
    return common_min, common_max


@lru_cache(maxsize=None)
def _magic_stat(common_max: int, base: int):
    magic_min = int(common_max + 1)
    magic_max = int(magic_min + base / 3)
    return magic_min, magic_max


@lru_cache(maxsize=None)
def _rare_stat(magic_max: int, base: int):
    rare_min = int(magic_max + 1)
    rare_max = int(rare_min + base / 2)
    return rare_min, rare_max


@lru_cache(maxsize=None)
def _legend_stat(rare_max: int, base: int):
    legend_min = int(rare_max + 1)
    legend_max = int(legend_min + base)
    return legend_min, legend_max


def _stats(level, rarity, base):
    common_min, common_max = _common_stat(base, level)
    if rarity == COMMON:
        return randint(common_min, common_max)
    magic_min, magic_max = _magic_stat(common_max, base)
    if rarity == UNCOMMON:
        return randint(magic_min, magic_max)
    rare_min, rare_max = _rare_stat(magic_max, base)
    if rarity == RARE:
        return randint(rare_min, rare_max)
    legend_min, legend_max = _legend_stat(rare_max, base)
    return randint(legend_min, legend_max)


def _get_name(rarity, item_type):
    if rarity == RARE:
        item_name_path = RARE_ITEM_NAME_PATH[item_type]
    else:
        item_name_path = ITEM_NAME_PATH[item_type]
    with open(item_name_path, encoding='utf-8') as items_name:
        names = items_name.read().splitlines()
    return choice(names).capitalize()


def _get_type():
    item_type = choice(TYPES)
    if item_type == WEAPON:
        item_type = choice(WEAPON_TYPES)
    return item_type


class Item:
    """Immutable Item class"""
    name: str
    type: str
    power: int
    level: int
    quality: str

    __slots__ = ('name', 'type', 'power', 'level',
                 'quality', 'embed')

    def _create_item(self, name: str, type_: str, power: int,
                     level: int, quality: str):
        """Create a Item instance."""
        if not isinstance(name, str):
            raise ValueError("'name' must be a string")
        if not isinstance(type_, str):
            raise ValueError("'type' must be a string")
        if not isinstance(power, int):
            raise ValueError("'power' must be a int")
        if not isinstance(level, int):
            raise ValueError("'level' must be a int")
        if not isinstance(quality, str):
            raise ValueError("'quality' must be a string")
        super().__setattr__('name', name)
        super().__setattr__('type', type_)
        super().__setattr__('power', power)
        super().__setattr__('level', level)
        super().__setattr__('quality', quality)

        embed = Embed(title=self.name,
                      color=COLOR[self.quality])
        embed.set_thumbnail(url=choice(IMG_LINKS))
        embed.add_field(name='Type', value=self.type)
        embed.add_field(name='Rareté', value=self.quality)
        embed.add_field(name='Niveau', value=str(self.level))
        embed.add_field(name='Puissance', value=f'{self.power:n}')
        super().__setattr__('embed', embed)

    def __init__(self, level: int = 1, rarity: Literal[0, 1, 2, 3] = 0,
                 json: Optional[dict] = None):
        """Create a Item instance."""
        if json:
            self._create_item(json['name'], json['type'], json['power'],
                              json['level'], json['quality'])
            return
        item_type = _get_type()
        rarity = _get_rarity(rarity)
        base = _get_base(level)
        stat = _stats(level, rarity, base)
        name = _get_name(rarity, item_type)
        self._create_item(name, item_type, stat, level, rarity)

    def __setattr__(self, name, value):
        """Prevent modification of attributes."""
        raise AttributeError('Item cannot be modified')

    def __repr__(self):
        """Create a string representation of the Item.
        You should always have at least __repr__ or __str__
        for interactive use.
        """
        template = "<Item(name='{}', rarity='{}', type='{}', power={})>"
        return template.format(
            self.name,
            self.quality,
            self.type,
            self.power,
        )

    def to_json(self):
        json = {
            'name': self.name,
            'type': self.type,
            'power': self.power,
            'level': self.level,
            'quality': self.quality,
        }
        return json


if __name__ == '__main__':
    stat_ = defaultdict(int)
    for _ in range(10000):
        stat_[_get_rarity(0)] += 1
    pprint(stat_)
