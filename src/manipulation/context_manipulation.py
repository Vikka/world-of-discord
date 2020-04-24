from typing import Tuple

from discord import Member, Guild
from discord.ext.commands import Context

from errors.guild import NoGuildError


def get_author_guild_from_context(context: Context) -> Tuple[Member, Guild]:
    guild: Guild = context.guild
    if not guild:
        raise NoGuildError
    author: Member = context.author
    return author, guild
