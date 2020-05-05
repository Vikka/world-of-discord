from discord.ext.commands import CommandError


class NotInCommandChannel(CommandError):
    pass


class IsDMChannel(CommandError):
    pass


class NotAdmin(CommandError):
    pass

class NotOwner(CommandError):
    pass