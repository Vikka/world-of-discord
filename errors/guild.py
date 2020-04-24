class NoGuildError(Exception):
    """The base exception type for errors that involve errors
    regarding unknown guild for a user.

    This inherits from :exc:`Exception`.
    """
    pass