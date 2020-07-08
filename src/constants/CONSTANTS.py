STAT_BASE = 9

DEFAULT_RANKING = 'membres'
GLOBAL_RANKING = 'guildes'
RANKING = [DEFAULT_RANKING, GLOBAL_RANKING]

DEFAULT_VALUE = 'niveaux'
LEVEL_VALUE = (DEFAULT_VALUE, 'level', 'niv', 'lvl')
EXP_VALUE = ('expérience', 'experience', 'exp', 'xp')
POWER_VALUE = ('puissance', 'power', 'pow')
KILLS_VALUE = ('tués', 'kills')
RARES_VALUE = ('rares',)
VALUE_ARRAY = [
    LEVEL_VALUE,
    EXP_VALUE,
    POWER_VALUE,
    KILLS_VALUE,
    RARES_VALUE,
]
VALUE = LEVEL_VALUE + EXP_VALUE + POWER_VALUE + KILLS_VALUE + RARES_VALUE
