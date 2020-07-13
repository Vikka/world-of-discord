"""
name_per_level.py
Created by dturba at 26/06/2020
"""
from random import randint
from typing import Optional

RARITY = ('common', 'rare')
item = {
    'name': str(),
    'icon': str(),
}
level = {
    'common': tuple(),
    'rare': tuple(),

}
ITEMS_PER_LEVEL = {
    2: {
        'common': (
            {
                'name': 'Rusted Hatchet',
                'icon': 'icon_1.png',
            }
        ),
        'rare': tuple()
    },
    6: {
        'common': ('Jade Hatchet',),
        'rare': ('The Screaming Eagle',),
    },
    11: {
        'common': ('Boarding Axe', 'Cleaver',),
        'rare': tuple()
    },
    16: {
        'common': tuple(),
        'rare': ('Dreadarc',)
    }
}


def get_item(level, i_rarity: int):
    possible_items = list()
    for i_level, items in ITEMS_PER_LEVEL.items():
        if i_level > level:
            break
        else:
            possible_items.extend(items[RARITY[i_rarity]])
    if not possible_items:
        possible_items = get_item(level, i_rarity - 1)
    return possible_items


def loot(level: int, rarity: Optional[int] = None):
    if rarity is None:
        rarity = randint(0, len(RARITY))
    possible_items = get_item(level, rarity)
    print(possible_items)


if __name__ == '__main__':
    loot(2)