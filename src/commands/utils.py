import os

from discord import DMChannel, Member
from discord.ext.commands import Context
from dotenv import load_dotenv

from errors.utils import NotInCommandChannel, NotAdmin

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
