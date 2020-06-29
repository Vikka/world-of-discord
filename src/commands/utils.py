import os

from discord import DMChannel, Member, Guild
from discord.ext.commands import Context
from dotenv import load_dotenv

from src.errors.utils import NotInCommandChannel, NotAdmin, NotOwner

load_dotenv()
ADMIN = int(os.getenv('ADMIN'))


def in_command_channel(context: Context) -> bool:
    if not isinstance(context.channel, DMChannel) \
            and context.channel.name != "commandes":
        raise NotInCommandChannel
    return True


def no_direct_message(context: Context) -> bool:
    if isinstance(context.channel, DMChannel):
        raise NotInCommandChannel
    return True


def is_admin(context: Context) -> bool:
    author: Member = context.author
    if author.id != ADMIN:
        raise NotAdmin
    return True


def is_owner(context: Context) -> bool:
    author: Member = context.author
    guild: Guild = context.guild
    if author != guild.owner:
        raise NotOwner
    return True


