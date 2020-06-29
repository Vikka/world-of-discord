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


def get_members_sorted(guild: Guild) -> List[Tuple[str, int]]:
    members = list()
    for member in guild.members:
        if (max_xp := get_max_xp(member)) > 0:
            members.append((member.name, get_max_xp(member)))
    return sorted(members, key=lambda x: x[1], reverse=True)


def create_embed_still(members: List[Tuple[str, int]], author: Member):
    numbers = list()
    names = list()
    exp_max = list()
    has_char = False
    author_pos = str()
    author_xp = str()
    for i, member in enumerate(members[:20], start=1):
        numbers.append(str(i))
        names.append(member[0])
        exp_max.append(f'{member[1]:n}')
    for i, member in enumerate(members, start=1):
        if member[0] == author.name:
            author_pos = i
            author_xp = member[1]
            has_char = True
            break

    numbers = '\n'.join(numbers)
    names = '\n'.join(names)
    exp_max = '\n'.join(exp_max)
    embed = Embed(title='Classement des membres')
    embed.add_field(name='n°', value=numbers)
    embed.add_field(name='Nom', value=names)
    embed.add_field(name='Exp max', value=exp_max)
    if has_char:
        embed.add_field(name='Position', value=f'{author_pos}')
        embed.add_field(name='xp maximum', value=f'{author_xp: n}')
    return embed


async def local_leaderboard(context: Context, guild: Guild, author: Member):
    await context.send(embed=create_embed_still(get_members_sorted(guild),
                                                author))
