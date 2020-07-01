RANDOM = 'Aléatoire'
COMMON = 'Commun'
UNCOMMON = 'Inhabituelle'
RARE = 'Rare'
LEGEND = 'Légendaire'

RARITY = (COMMON, UNCOMMON, RARE, LEGEND)

WEAPON = 'Arme'
HELMET = 'Casque'
LEGS = 'Jambières'
BOOTS = 'Bottes'
CHEST = 'Plastron'
GLOVES = 'Gants'
BELT = 'Ceinture'
CLOAK = 'Cape'
SHOULDERS = 'Epauliers'
WRIST = 'Brassards'
RING = 'Anneaux'
TRINKET = 'Babiole'
SHIELD = 'Bouclier'

BOW = 'Arc'
DAGGER = 'Dague'
MACE = 'Masse'
SWORD = 'Epée'

COMMON_COLOR = 0xbfbfbf
MAGIC_COLOR = 0x4258ff
RARE_COLOR = 0xfdd023
LEGEND_COLOR = 0xff755d

COLOR = {
    COMMON: COMMON_COLOR,
    UNCOMMON: MAGIC_COLOR,
    RARE: RARE_COLOR,
    LEGEND: LEGEND_COLOR,
}

TYPES = [
    [WEAPON, HELMET, LEGS, BOOTS],
    [CHEST, GLOVES],
    [BELT, CLOAK],
    [SHOULDERS, WRIST],
    [RING],
]
WEAPON_TYPES = [BOW, DAGGER, MACE, SWORD]

RARITY_PROB = (
    (RANDOM, 0),
    (COMMON, 0),
    (UNCOMMON, 0.5),
    (RARE, 1),
)

# RARITY_PROB = (
#     (RANDOM, 0),
#     (COMMON, 0.98),
#     (UNCOMMON, 0.999),
#     (RARE, 0.99999),
#     (LEGEND, 1),
# )
