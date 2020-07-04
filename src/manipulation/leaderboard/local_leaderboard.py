from typing import Tuple, List

from discord import Guild, Member
from discord.ext.commands import Context

from src.errors.character import NoRecordedPlayers
from src.manipulation.character_manipulation import get_path_and_characters
from src.manipulation.leaderboard.utils import create_embed


def get_max_xp(member: Member):
    path, characters = get_path_and_characters(member, member.guild)
    max_xp = 0
    name = ''
    for character in characters.values():
        if character.total_exp > max_xp:
            name = character._name
            max_xp = character.total_exp
    return max_xp, name


def get_members_sorted(guild: Guild) -> List[Tuple[str, str, int]]:
    members = list()
    for member in guild.members:
        max_xp, name = get_max_xp(member)
        if max_xp > 0:
            members.append((member.name, name, max_xp))
    if not members:
        raise NoRecordedPlayers
    return sorted(members, key=lambda x: x[2], reverse=True)


async def local_leaderboard(context: Context, guild: Guild, author: Member):
    await context.send(embed=create_embed(get_members_sorted(guild),
                                          author, 0))
