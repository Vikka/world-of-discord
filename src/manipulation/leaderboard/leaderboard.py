from collections import namedtuple
from typing import List, Tuple, Optional, Union

from discord import Embed, Guild, Member

from src.classes.Character import get_path_and_characters
from src.constants.CONSTANTS import VALUE_ARRAY, GUILDS_RANKING, \
    MEMBERS_RANKING, RANKING_ARRAY, WORLD_RANKING
from src.errors.character import NoRecordedPlayers
from src.utils.utils import first

Leaderboard = namedtuple('Leaderboard', ['id', 'name', 'value'])


def member_max_value(member: Member, key: str) -> Tuple[int, str]:
    path, characters = get_path_and_characters(member, member.guild)
    max_value = 0
    name = ''

    for character in characters.values():
        if character.get_value(key) > max_value:
            name = character._name
            max_value = character.get_value(key)
    return max_value, name


def guild_max_value(guild: Guild, key: str) -> int:
    max_exp = 0

    for member in guild.members:
        tmp_xp, _ = member_max_value(member, key)
        max_exp = max(max_exp, tmp_xp)
    return max_exp


def get_members(guild: Guild, key: str) -> List[Leaderboard]:
    members = list()

    for member in guild.members:
        value, name = member_max_value(member, key)
        if value > 0:
            members.append(Leaderboard(member.id, name, value))
    if not members:
        raise NoRecordedPlayers
    return sorted(members,
                  key=lambda x: x.value,
                  reverse=True)


def get_guilds(guilds: List[Guild], key: str) -> List[Leaderboard]:
    return sorted((Leaderboard(guild.id, guild.name, max_xp)
                   for guild in guilds
                   if (max_xp := guild_max_value(guild, key))),
                  key=lambda x: x.value,
                  reverse=True)


def get_world_members(guilds: List[Guild], key: str) -> List[Leaderboard]:
    members = list()
    for guild in guilds:
        try:
            members.extend(get_members(guild, key))
        except NoRecordedPlayers:
            pass
    if not members:
        raise NoRecordedPlayers
    return sorted(members,
                  key=lambda x: x.value,
                  reverse=True)


def get_ranking(members, id_) -> Tuple[list, list, list]:
    numbers = list()
    names = list()
    values = list()

    for i, member in enumerate(members[:20], start=1):
        bold_str = f'{"**" if member.id == id_ else ""}'
        numbers.append(f'{bold_str}{i}{bold_str}')
        names.append(f'{bold_str}{member[1]}{bold_str}')
        values.append(f'{bold_str}{member[2]:,}{bold_str}')
    return numbers, names, values


def get_author(members: List[Leaderboard], id_: int) \
        -> Tuple[Optional[int], Optional[int], bool]:
    for i, member in enumerate(members, start=1):
        if member.id == id_:
            return i, member.value, True
    return None, None, False


def create_embed(members: List[Leaderboard], author: Member,
                 ranking_type: str, key: str) -> Embed:
    """
    Thanks to StillinBed for his help !
    """
    ranking_type = first(
        RANKING_ARRAY,
        lambda iterable: ranking_type in iterable
    )[0]
    id_: int = author.id if ranking_type in MEMBERS_RANKING else author.guild.id
    numbers, names, values = get_ranking(members, id_)
    author_pos, author_value, has_char = get_author(members, id_)
    numbers = '\n'.join(numbers)
    names = '\n'.join(names)
    exp_max = '\n'.join(values)
    key = first(VALUE_ARRAY, lambda iterable: key in iterable)[0].capitalize()

    embed = Embed(title=f'Classement {ranking_type}')
    embed.add_field(name='n°', value=numbers)
    embed.add_field(name='Nom', value=names)
    embed.add_field(name=key, value=exp_max)
    if has_char:
        embed.add_field(name='Position', value=f'{author_pos}')
        embed.add_field(name=key, value=f'{author_value:,}')
    return embed


switch = {
    MEMBERS_RANKING: get_members,
    GUILDS_RANKING: get_guilds,
    WORLD_RANKING: get_world_members,
}


def leaderboard_embed(guilds: Union[Guild, List[Guild]], author: Member,
                      ranking_type: str, value_type: str) -> Embed:
    ranking_func = switch.get(
        first(switch,
              lambda ranking_names: ranking_type in ranking_names)
    )
    return create_embed(ranking_func(guilds, value_type), author, ranking_type,
                        value_type)
