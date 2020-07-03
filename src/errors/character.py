from discord.ext.commands import UserInputError


class TwoManyCharacters(UserInputError):
    """The base exception type for errors that involve errors
    regarding too many characters for a user.

    This inherits from :exc:`UserInputError`.
    """
    pass


class UnknownCharacters(UserInputError):
    """The base exception type for errors that involve errors
    regarding unknown characters for a user.

    This inherits from :exc:`UserInputError`.
    """
    pass


class NoCharacters(Exception):
    """The base exception type for errors that involve errors
    regarding too few characters for a user.

    This inherits from :exc:`Exception`.
    """
    pass


class NoLeader(Exception):
    """The base exception type for errors that involve errors
    regarding the lack of leader in user's characters.

    This inherits from :exc:`Exception`.
    """
    pass


class CharactersLocked(Exception):
    """The base exception type for errors that involve errors
    regarding the lockness of a user's character.

    This inherits from :exc:`Exception`.
    """
    pass


class CharacterAlreadyExist(UserInputError):
    """This inherits from :exc:`UserInputError`."""
    pass


class NoRecordedPlayers(Exception):
    pass
