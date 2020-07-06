from discord.ext.commands import CommandError


class GuildError(CommandError):
    pass


class NoGuildError(GuildError):
    pass


class ChannelAlreadyExist(GuildError):
    pass
