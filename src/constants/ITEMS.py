RANDOM = 'Aléatoire'
COMMON = 'Commun'
MAGIC = 'Magique'
RARE = 'Rare'
LEGEND = 'Légendaire'

WEAPON = 'Arme'
HELMET = 'Casque'
LEGS = 'Jambières'
BOOTS = 'Bottes'

BOWS = 'Arc'
DAGGERS = 'Dague'
MACES = 'Masse'
SWORDS = 'Epée'

COMMON_COLOR = 0xbfbfbf
MAGIC_COLOR = 0x4258ff
RARE_COLOR = 0xfdd023
LEGEND_COLOR = 0xff755d


COLOR = {
    COMMON: COMMON_COLOR,
    MAGIC: MAGIC_COLOR,
    RARE: RARE_COLOR,
    LEGEND: LEGEND_COLOR,
}

TYPES = [WEAPON, HELMET, LEGS, BOOTS]
WEAPON_TYPES = [BOWS, DAGGERS, MACES, SWORDS]

RARITY = (
    (RANDOM, 0),
    (COMMON, 0.25),
    (MAGIC, 0.50),
    (RARE, 1),
)

# RARITY = (
#     (RANDOM, 0),
#     (COMMON, 0.98),
#     (MAGIC, 0.999),
#     (RARE, 0.99999),
#     (LEGEND, 1),
# )
