"""
ITEMS.py
Created by dturba at 26/06/2020
"""
from collections import namedtuple
from random import choice

from src.constants.ITEMS_UTILS import BOW, DAGGER, COMMON, RARE, RARITY, \
    UNCOMMON, MACE

Item = namedtuple('Item', ['name', 'icon_path'])

ITEMS = [
    {
        COMMON: {
            DAGGER: Item('Couteau à dépecer', 'dagger_icon_1'),
            MACE: Item('Gourdin lourd', 'mace_icon_1')
        },
    },
    {},
    {
        UNCOMMON: {
            DAGGER: Item("Épée longue de l'armée Gnome", 'dagger_icon_2'),
        },
    },
    {
        UNCOMMON: {
            MACE: Item('Fracasse-Crâne', 'mace_icon_2'),
        },
    },
    {
        COMMON: {
            DAGGER: Item('Stylet', 'dagger_icon_2'),
        },
    },
    {},
    {
        UNCOMMON: {
            DAGGER: Item('Croc de veuve', 'dagger_icon_2'),
        },
    },
    {
        RARE: {
            DAGGER: Item('Bistouri de Calen', 'dagger_icon_2'),
        },
    },
    {
        COMMON: {
            DAGGER: Item('Couteau à écorcher', 'dagger_icon_3'),
        },
    },
    {},
    {},
    {
        UNCOMMON: {
            DAGGER: Item('Poignard luisant', 'dagger_icon_2'),
        },
    },
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
]


def get_all_items_from_type(item_type: str, i_rarity: int):
    if i_rarity == -1:
        total = list()
        for i in range(4):
            total.extend(get_all_items_from_type(item_type, i))
        total.sort(key=lambda x: x[0])
        return total
    return [(i, item.name, RARITY[i_rarity]) for i, items in enumerate(ITEMS) if RARITY[i_rarity] in items for type_, item in items[RARITY[i_rarity]].items() if type_ == item_type]


def get_possible_items(level: int, i_rarity: int):
    possible_items = list()
    for i, item in enumerate(ITEMS[:level]):
        if RARITY[i_rarity] in item:
            possible_items.append((i, item.get(RARITY[i_rarity])))
    return possible_items if possible_items else get_possible_items(level, i_rarity - 1)


def get_item(level: int, i_rarity: int):
    return choice(get_possible_items(level, i_rarity))


if __name__ == '__main__':
    print(get_item(20, 1))
    print(get_all_items_from_type(DAGGER, -1))
