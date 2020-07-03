from typing import Tuple, List

from discord import Guild, Member
from discord.ext.commands import Context

from src.errors.character import NoRecordedPlayers
from src.manipulation.character_manipulation import get_path_and_characters
from src.manipulation.leaderboard.utils import create_embed


def get_max_xp(member: Member):
    path, characters = get_path_and_characters(member, member.guild)
    max_xp = 0
    for character in characters.values():
        max_xp = max(character.total_exp, max_xp)
    return max_xp


def get_members_sorted(guild: Guild) -> List[Tuple[str, int]]:
    members = list()
    for member in guild.members:
        if (max_xp := get_max_xp(member)) > 0:
            members.append((member.name, max_xp))
    if not members:
        raise NoRecordedPlayers
    return sorted(members, key=lambda x: x[1], reverse=True)


async def local_leaderboard(context: Context, guild: Guild, author: Member):
    await context.send(embed=create_embed(get_members_sorted(guild),
                                          author, 0))
