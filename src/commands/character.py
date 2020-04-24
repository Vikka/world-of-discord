import re

from discord.ext.commands import Cog, Context, command, BadArgument, \
    MissingRequiredArgument

from errors.character import TwoManyCharacters, UnknownCharacters, NoCharacters, \
    CharacterAlreadyExist
from src.classes.Character import Character
from src.constants.REGEX import NAME_PATTERN
from src.manipulation.character_manipulation import _get_path_and_characters, \
    _store_characters
from src.manipulation.context_manipulation import get_author_guild_from_context

name_pattern = re.compile(NAME_PATTERN)


def is_name(name):
    """For command annotation"""
    if not name_pattern.match(name):
        raise BadArgument
    return name


class Personnage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='creer', usage='<Prénom> | <Prénom Nom>',
             aliases=['créer', 'create'])
    async def create(self, context: Context, *, name: is_name):
        """
        Enregistre un nouveau personnage.

        Te permet de créer un personnage lié au serveur sur lequel tu
        effectues cette commande. Tu peux créer jusqu'à 3 personnages.
        """
        author, guild = get_author_guild_from_context(context)
        path, characters = _get_path_and_characters(author, guild)

        if len(characters) > 2:
            raise TwoManyCharacters

        for character in characters.values():
            character._current = False

        if name in characters:
            raise CharacterAlreadyExist

        characters[name] = Character(name)
        _store_characters(path, characters)
        await context.send(f'{name} créé·e avec succès !')

    @command(name='supprimer', usage='<Prénom> | <Prénom Nom>',
             aliases=['suppr', 'delete', 'del'])
    async def delete(self, context: Context, *, name: is_name):
        """
        Supprime un de tes personnages.

        Te permet de supprimer un de tes personnages lié au serveur sur lequel
        tu effectues cette commande. Tu peux avoir jusqu'à 3 personnages.
        """
        author, guild = get_author_guild_from_context(context)
        path, characters = _get_path_and_characters(author, guild)

        if name not in characters:
            raise UnknownCharacters

        characters.pop(name)
        leader_flag = False
        for character in characters.values():
            if character._current:
                leader_flag = True
                break
        if not leader_flag and characters:
            list(characters.values())[0]._current = True

        _store_characters(path, characters)
        await context.send(f'{name} supprimé·e avec succès !')

    @command(name='lister', aliases=['liste', 'list'])
    async def list(self, context: Context):
        """
        Liste vos personnages.

        Te permet de supprimer un de tes personnages lié au serveur sur lequel
        tu effectues cette commande. Tu peux avoir jusqu'à 3 personnages.
        """
        author, guild = get_author_guild_from_context(context)
        _, characters = _get_path_and_characters(author, guild)

        if len(characters) < 1:
            raise NoCharacters

        char_list = ',\n\t'.join(character for character in characters.keys())
        await context.send(f'Voici la liste de tes personnages :\n\t'
                           f'{char_list}.')

    @create.error
    async def create_error(self, context: Context, error):
        if isinstance(error, BadArgument):
            await context.send("Le format de nom n'est pas bon, désolé.\n"
                               "Test le format de ton nom ici : "
                               "https://regex101.com/r/GWsaBf/2\n"
                               f"N'hésite pas à taper la commande \"!help créer\" "
                               "pour avoir de l'aide.")
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom (tu peux aussi préciser le nom) !\n"
                "N'hésite pas à taper la commande \"!help creer\" pour avoir "
                "de l'aide.")
        if isinstance(error, TwoManyCharacters):
            await context.send(
                "Tu ne peux créer que 3 personnages.\n"
                "N'hésite pas à taper la commande \"!help creer\" pour avoir "
                "de l'aide.")
        if isinstance(error, CharacterAlreadyExist):
            await context.send(
                "Le personnage que tu souhaites créer existe déjà !")
    @delete.error
    async def delete_error(self, context: Context, error):
        if isinstance(error, BadArgument):
            await context.send("Le format de nom n'est pas bon, désolé.\n"
                           "Test le format de ton nom ici : "
                           "https://regex101.com/r/GWsaBf/2\n"
                           f"N'hésite pas à taper la commande "
                           f"\"!help supprimer\" pour avoir de l'aide.")
        if isinstance(error, UnknownCharacters):
            await context.send(
                "Le personnage est introuvable.\n"
                "N'hésite pas à taper la commande \"!help supprimer\" pour "
                "avoir de l'aide.")
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom exact (nom si il y a, aussi) !\n"
                "N'hésite pas à taper la commande \"!help supprimer\" pour "
                "avoir de l'aide.")

    @list.error
    async def list_error(self, context: Context, error):
        if isinstance(error, NoCharacters):
            await context.send(
                "Tu n'a aucun personnage.\n"
                "N'hésite pas à taper la commande \"!help Personnage\" pour "
                "avoir de l'aide.")


def setup(bot):
    bot.add_cog(Personnage(bot))