from discord.ext.commands import UserInputError, CommandError


class TwoManyCharacters(UserInputError):
    pass


class UnknownCharacters(UserInputError):
    pass


class NoCharacters(CommandError):
    pass


class NoLeader(CommandError):
    pass


class CharactersLocked(CommandError):
    pass


class CharacterAlreadyExist(UserInputError):
    pass


class NoRecordedPlayers(Exception):
    pass
