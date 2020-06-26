from typing import List, Tuple

from discord import Guild, Embed
from discord.ext.commands import Context

from src.manipulation.character_manipulation import get_path_and_characters


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
        guild_list.append((guild.name, _max_xp(guild)))
    return sorted(guild_list, key=lambda x: x[1], reverse=True)


def _create_embed(guild_list: List[Tuple[str, int]]):
    """
    TODO: améliorer l'embed
    """
    embed = Embed(title='Classement des Guildes')
    embed.add_field(name='n°', value=str(1))
    embed.add_field(name='Nom', value=guild_list[0][0])
    embed.add_field(name='Exp max', value=str(guild_list[0][1]))
    names = 1
    complete = True
    for i, guild in enumerate(guild_list[1:], start=2):
        if i % 2 == 0:
            names = (str(i), guild[0], guild[1])
            complete = False
            continue
        embed.add_field(name=names[0], value=str(i))
        embed.add_field(name=names[1], value=guild[0])
        embed.add_field(name=names[2], value=str(guild[1]))
        complete = True
    if not complete:
        embed.add_field(name=names[0], value='\u200b')
        embed.add_field(name=names[1], value='\u200b')
        embed.add_field(name=names[2], value='\u200b')
    return embed


async def global_leaderboard(context: Context, guilds: List[Guild]):
    if not guilds:
        return
    await context.send(embed=_create_embed(_guild_xp_sorted(guilds)))
