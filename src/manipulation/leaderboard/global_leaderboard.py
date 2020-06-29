from typing import List, Tuple

from discord import Guild, Member
from discord.ext.commands import Context

from src.manipulation.character_manipulation import get_path_and_characters
from src.manipulation.leaderboard.utils import create_embed


def _max_xp(guild: Guild) -> int:
    max_exp = 0
    for member in guild.members:
        path, characters = get_path_and_characters(member, guild)
        tmp_exp = 0
        for character in characters.values():
            tmp_exp = max(character.total_exp, tmp_exp)
        max_exp = max(tmp_exp, max_exp)
    return max_exp


def _guild_xp_sorted(guilds: List[Guild]) -> List[Tuple[str, int]]:
    guild_list = list()
    for guild in guilds:
        if max_xp := _max_xp(guild):
            guild_list.append((guild.name, max_xp))
    return sorted(guild_list, key=lambda x: x[1], reverse=True)


async def global_leaderboard(context: Context, guilds: List[Guild],
                             author: Member):
    if not guilds:
        return
    await context.send(embed=create_embed(_guild_xp_sorted(guilds),
                                          author, 1))
