from collections import namedtuple
from typing import List, Tuple, Optional, Union

from discord import Embed, Guild, Member

from constants.CONSTANTS import DEFAULT_RANKING, GLOBAL_RANKING
from errors.character import NoRecordedPlayers
from manipulation.character_manipulation import get_path_and_characters

Leaderboard = namedtuple('Leaderboard', ['id', 'name', 'value'])


def member_max_xp(member: Member) -> Tuple[int, str]:
    path, characters = get_path_and_characters(member, member.guild)
    max_xp = 0
    name = ''

    for character in characters.values():
        if character.total_exp > max_xp:
            name = character._name
            max_xp = character.total_exp
    return max_xp, name


def guild_max_xp(guild: Guild) -> int:
    max_exp = 0

    for member in guild.members:
        tmp_xp, _ = member_max_xp(member)
        max_exp = max(max_exp, tmp_xp)
    return max_exp


def get_members(guild: Guild) -> List[Tuple[int, str, int]]:
    members = list()

    for member in guild.members:
        max_xp, name = member_max_xp(member)
        if max_xp > 0:
            members.append(Leaderboard(member.id, name, max_xp))
    if not members:
        raise NoRecordedPlayers
    return sorted(members,
                  key=lambda x: x.value,
                  reverse=True)


def get_guilds(guilds: List[Guild]) -> List[Leaderboard]:
    return sorted((Leaderboard(guild.id, guild.name, max_xp)
                   for guild in guilds
                   if (max_xp := guild_max_xp(guild))),
                  key=lambda x: x.value,
                  reverse=True)


def get_ranking(members, id_) -> Tuple[list, list, list]:
    numbers = list()
    names = list()
    values = list()

    for i, member in enumerate(members[:20], start=1):
        flag = member.id == id_
        borld_str = f'{"**" if flag else ""}'
        numbers.append(f'{borld_str}{i}{borld_str}')
        names.append(f'{borld_str}{member[1]}{borld_str}')
        values.append(f'{borld_str}{member[2]:,}{borld_str}')
    return numbers, names, values


def get_author(members: List[Leaderboard], id_: int) \
        -> Tuple[Optional[int], Optional[int], bool]:
    for i, member in enumerate(members, start=1):
        if member.id == id_:
            return i, member.value, True
    return None, None, False


def create_embed(members: List[Leaderboard], author: Member,
                 ranking_type: str) -> Embed:
    """
    Thanks to StillinBed for his help !
    """
    id_: int = author.id if ranking_type == "membres" else author.guild.id
    numbers, names, values = get_ranking(members, id_)
    author_pos, author_xp, has_char = get_author(members, id_)
    numbers = '\n'.join(numbers)
    names = '\n'.join(names)
    exp_max = '\n'.join(values)

    embed = Embed(title=f'Classement des {ranking_type}')
    embed.add_field(name='n°', value=numbers)
    embed.add_field(name='Nom', value=names)
    embed.add_field(name='Exp max', value=exp_max)
    if has_char:
        embed.add_field(name='Position', value=f'{author_pos}')
        embed.add_field(name='xp maximum', value=f'{author_xp:,}')
    return embed


switch = {
    DEFAULT_RANKING: get_members,
    GLOBAL_RANKING: get_guilds,
}


def leaderboard_embed(guilds: Union[Guild, List[Guild]], author: Member,
                      ranking_type: str) -> Embed:
    ranking_func = switch.get(ranking_type, get_members)
    return create_embed(ranking_func(guilds), author, ranking_type)
