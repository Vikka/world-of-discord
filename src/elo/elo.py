from math import log
from statistics import mean
from typing import Literal

bonus_table = {
    1.0: 800, .99: 677, .98: 589, .97: 538, .96: 501, .95: 470, .94: 444,
    .93: 422, .92: 401, .91: 383, .90: 366, .89: 351, .88: 336, .87: 322,
    .86: 309, .85: 296, .84: 284, .83: 273, .82: 262, .81: 251, .80: 240,
    .79: 230, .78: 220, .77: 211, .76: 202, .75: 193, .74: 184, .73: 175,
    .72: 166, .71: 158, .70: 149, .69: 141, .68: 133, .67: 125, .66: 117,
    .65: 110, .64: 102, .63: 95, .62: 87, .61: 80, .60: 72, .59: 65, .58: 57,
    .57: 50, .56: 43, .55: 36, .54: 29, .53: 21, .52: 14, .51: 7, .50: 0,
    .49: -7, .48: -14, .47: -21, .46: -29, .45: -36, .44: -43, .43: -50,
    .42: -57, .41: -65, .40: -72, .39: -80, .38: -87, .37: -95, .36: -102,
    .35: -110, .34: -117, .33: -125, .32: -133, .31: -141, .30: -149, .29: -158,
    .28: -166, .27: -175, .26: -184, .25: -193, .24: -202, .23: -211, .22: -220,
    .21: -230, .20: -240, .19: -251, .18: -262, .17: -273, .16: -284, .15: -296,
    .14: -309, .13: -322, .12: -336, .11: -351, .10: -366, .09: -383, .08: -401,
    .07: -422, .06: -444, .05: -470, .04: -501, .03: -538, .02: -589, .01: -677,
    .00: -800,
}


def compute_bonus(ratio: float, min_: int = -800, max_: int = 800) -> int:
    if ratio == 0:
        return min_
    if ratio == 1:
        return max_
    return round(-371.5 * log(1 / ratio - 1, 10))


def compute_initial_elo(results: list, victories: int,
                        table: bool = True) -> int:
    bonus = bonus_table[float(f'{victories / len(results):.2f}')] if table \
        else compute_bonus(victories / len(results), -1000, 1000)
    return round(mean(results) + bonus)


def _get_coef(total_games: int, elo: int) -> Literal[10, 30, 40]:
    if total_games < 30:
        return 40
    if elo < 2400:
        return 30
    return 10


def compute_new_elo(total_games: int, elo: int, opponent_elo: int, win: float):
    coef = _get_coef(total_games, elo)
    elo_diff = tmp if (tmp := elo - opponent_elo) < 400 else 400
    score_probability = 1 / (1 + pow(10, -elo_diff / 400))
    new_elo = round(elo + coef * (win - score_probability))
    return new_elo


if __name__ == '__main__':
    # results_ = [
    #     1500,
    #     1500,
    #     1700,
    #     1700,
    #     1600,
    # ]
    # victories_ = 5
    # initial_elo = compute_initial_elo(results_, victories_, table=False)
    # print(initial_elo)
    # new_elo_ = compute_new_elo(30, initial_elo, 1150, 1)
    # print(new_elo_)
    new_elo_ = compute_new_elo(1, 0, 0, 1)
    print(new_elo_)