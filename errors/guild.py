class GuildError(Exception):
    """The base exception type for errors that involve errors
    regarding guilds.

    This inherits from :exc:`Exception`.
    """
    pass


class NoGuildError(GuildError):
    pass


class ChannelAlreadyExist(GuildError):
    pass
