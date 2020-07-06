from typing import Tuple, List

from discord import Embed, Member


def leaderboard_init(type_: int) -> Tuple[List, List, List, bool, str, str,
                                          str]:
    leaderboard_type = {
        0: 'membres',
        1: 'guildes',
    }
    return list(), list(), list(), False, str(), str(), leaderboard_type[type_]


def create_embed(members: List[Tuple[int, str, int]], author: Member,
                 type_: int):
    """
    Thanks to StillinBed for his help !
    """
    numbers, names, exp_max, has_char, author_pos, author_xp, type_ \
        = leaderboard_init(type_)
    for i, member in enumerate(members[:20], start=1):
        numbers.append(str(i))
        names.append(member[1])
        exp_max.append(f'{member[2]:,}')
    for i, member in enumerate(members, start=1):
        if member[0] == (author.id if type_ == "membres" else author.guild.id):
            author_pos = i
            author_xp = member[2]
            has_char = True
            break
    numbers = '\n'.join(numbers)
    names = '\n'.join(names)
    exp_max = '\n'.join(exp_max)
    embed = Embed(title=f'Classement des {type_}')
    embed.add_field(name='n°', value=numbers)
    embed.add_field(name='Nom', value=names)
    embed.add_field(name='Exp max', value=exp_max)
    if has_char:
        embed.add_field(name='Position', value=f'{author_pos}')
        embed.add_field(name='xp maximum', value=f'{author_xp:,}')
    return embed
