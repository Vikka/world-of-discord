from discord import DMChannel
from discord.ext.commands import Context

from errors.utils import NotInCommandChannel


def in_command_channel(context: Context):
    if not isinstance(context.channel, DMChannel)\
            and context.channel.name != "commandes":
        raise NotInCommandChannel
    return True


def no_direct_message(context: Context):
    if isinstance(context.channel, DMChannel):
        raise NotInCommandChannel
    return True
