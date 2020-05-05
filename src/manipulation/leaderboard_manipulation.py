from typing import List

from discord import Guild, Embed
from discord.ext.commands import Context

from src.manipulation.character_manipulation import _get_path_and_characters


async def global_leaderboard(context: Context, guilds: List[Guild]):
    if not guilds:
        return
    guild_list = list()
    for guild in guilds:
        max_exp = 0
        for member in guild.members:
            path, characters = _get_path_and_characters(member, guild)
            tmp_exp = 0
            for character in characters.values():
                tmp_exp = max(character.total_exp, tmp_exp)
            max_exp = max(tmp_exp, max_exp)
        guild_list.append((guild.name, max_exp))
    guild_list.sort(key=lambda x: x[1], reverse=True)
    embed = Embed(title='Classement des Guildes')
    embed.add_field(name='n°', value=str(1))
    embed.add_field(name='Nom', value=guild_list[0][0])
    embed.add_field(name='Exp max', value=guild_list[0][1])
    names = 1
    complet = True
    for i, guild in enumerate(guild_list[1:], start=2):
        if i % 2 == 0:
            names = (str(i), guild[0], guild[1])
            complet = False
            continue
        embed.add_field(name=names[0], value=str(i))
        embed.add_field(name=names[1], value=guild[0])
        embed.add_field(name=names[2], value=guild[1])
        complet = True
    if not complet:
        embed.add_field(name=names[0], value='\u200b')
        embed.add_field(name=names[1], value='\u200b')
        embed.add_field(name=names[2], value='\u200b')
    await context.send(embed=embed)