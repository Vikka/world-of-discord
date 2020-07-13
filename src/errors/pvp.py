from discord import Forbidden
from discord.ext.commands import CommandError


class AlreadyRegistered(CommandError):
    pass


class OnlyOneCharacter(AlreadyRegistered):
    pass

class NoDM(CommandError, Forbidden):
    pass