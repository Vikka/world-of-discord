STAT_BASE = 9

DEFAULT_RANKING = 'membres'
MEMBERS_RANKING = (DEFAULT_RANKING, 'membre', 'members', 'member', 'm')
GUILDS_RANKING = ('guildes', 'guilde', 'guilds', 'guild', 'g')
RANKING_ARRAY = [
    MEMBERS_RANKING,
    GUILDS_RANKING
]
RANKING = MEMBERS_RANKING + GUILDS_RANKING

DEFAULT_VALUE = 'niveaux'
LEVEL_VALUE = (DEFAULT_VALUE, 'level', 'niv', 'lvl', 'n', 'l')
EXP_VALUE = ('expérience', 'experience', 'exp', 'xp', 'e', 'x')
POWER_VALUE = ('puissance', 'power', 'pow', 'p')
KILLS_VALUE = ('tués', 'kills', 't', 'k')
RARES_VALUE = ('rares', 'rare', 'r')
DUEL_VALUE = ('duels', 'duel', 'dudu', 'd')
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
