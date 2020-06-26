from typing import Tuple, List

from discord import Guild, Member, Embed
from discord.ext.commands import Context

from src.manipulation.character_manipulation import get_path_and_characters


def get_max_xp(member: Member):
    path, characters = get_path_and_characters(member, member.guild)
    max_xp = 0
    for character in characters.values():
        max_xp = max(character.total_exp, max_xp)
    return max_xp


def get_members_sorted(guild: Guild):
    members = list()
    for member in guild.members:
        if (max_xp := get_max_xp(member)) > 0:
            members.append((member.name, get_max_xp(member)))
    return sorted(members, key=lambda x: x[1], reverse=True)


def create_embed(members: List[Tuple[str, int]]):
    """
    TODO: améliorer l'embed
    """
    embed = Embed(title='Classement des membres')
    embed.add_field(name='n°', value=str(1))
    embed.add_field(name='Nom', value=members[0][0])
    embed.add_field(name='Exp max', value=str(members[0][1]))
    names = 1
    complete = True
    for i, member in enumerate(members[1:], start=2):
        if i % 2 == 0:
            names = (str(i), member[0], member[1])
            complete = False
            continue
        embed.add_field(name=names[0], value=str(i))
        embed.add_field(name=names[1], value=member[0])
        embed.add_field(name=names[2], value=str(member[1]))
        complete = True
    if not complete:
        embed.add_field(name=names[0], value='\u200b')
        embed.add_field(name=names[1], value='\u200b')
        embed.add_field(name=names[2], value='\u200b')
    return embed


async def local_leaderboard(context: Context, guild: Guild):
    await context.send(embed=create_embed(get_members_sorted(guild)))
