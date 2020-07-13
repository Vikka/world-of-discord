STAT_BASE = 9

DEFAULT_RANKING = 'membres'
MEMBERS_RANKING = (DEFAULT_RANKING, 'membre', 'members', 'member', 'm')
GUILDS_RANKING = ('guildes', 'guilde', 'guilds', 'guid', 'g')
RANKING_ARRAY = [
    MEMBERS_RANKING,
    GUILDS_RANKING
]
RANKING = MEMBERS_RANKING + GUILDS_RANKING

DEFAULT_VALUE = 'niveaux'
LEVEL_VALUE = (DEFAULT_VALUE, 'level', 'niv', 'lvl')
EXP_VALUE = ('expérience', 'experience', 'exp', 'xp')
POWER_VALUE = ('puissance', 'power', 'pow')
KILLS_VALUE = ('tués', 'kills')
RARES_VALUE = ('rares',)
DUEL_VALUE = ('duels', 'duel', 'dudu')
VALUE_ARRAY = [
    LEVEL_VALUE,
    EXP_VALUE,
    POWER_VALUE,
    KILLS_VALUE,
    RARES_VALUE,
    DUEL_VALUE,
]
VALUE = LEVEL_VALUE + EXP_VALUE + POWER_VALUE + KILLS_VALUE + RARES_VALUE \
        + DUEL_VALUE
