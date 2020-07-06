import re
from typing import Optional

from discord.ext.commands import Cog, Context, command, BadArgument, \
    MissingRequiredArgument, Bot, CommandInvokeError

from src.classes.Character import Character
from src.commands.utils import no_direct_message, in_command_channel
from src.constants.CONSTANTS import RANKING, GLOBAL_RANKING, DEFAULT_RANKING
from src.constants.REGEX import NAME_PATTERN, NAME_PATTERN_LINK
from src.errors.character import TwoManyCharacters, UnknownCharacters, \
    NoCharacters, CharacterAlreadyExist, NoRecordedPlayers
from src.manipulation.character_manipulation import get_path_and_characters, \
    store_characters, get_leader
from src.manipulation.context_manipulation import get_author_guild_from_context
from src.manipulation.leaderboard.global_leaderboard import global_leaderboard
from src.manipulation.leaderboard.local_leaderboard import local_leaderboard

name_pattern = re.compile(NAME_PATTERN, flags=re.I)


def is_name(name: str) -> str:
    """For command annotation"""
    if not name:
        return ''
    if not name_pattern.match(name):
        raise BadArgument
    return name.lower().capitalize()


def ranking_type(type_: str):
    """For command annotation"""
    if not type_:
        return DEFAULT_RANKING
    if type_ not in RANKING:
        raise BadArgument
    return type_


def _init_data(context: Context):
    author, guild = get_author_guild_from_context(context)
    path, characters = get_path_and_characters(author, guild)
    return author, guild, path, characters


class Personnage(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command(name='creer', usage='<Prénom> | <Prénom Nom>',
             aliases=['créer', 'create'],
             checks=[no_direct_message, in_command_channel])
    async def create(self, context: Context, *, name: is_name):
        """
        Enregistre un nouveau personnage.

        Te permet de créer un personnage lié au serveur sur lequel tu
        effectues cette commande. Tu peux créer jusqu'à 1 personnages.
        """
        author, guild, path, characters = _init_data(context)

        if len(characters) > 0:
            raise TwoManyCharacters

        for character in characters.values():
            character.is_leader = False
        name = name.lower().capitalize()
        if name in characters:
            raise CharacterAlreadyExist

        id_ = f'{guild.id}-{author.id}-{name}'
        characters[id_] = Character(id_, name)
        store_characters(path, characters)
        await context.send(f'{name} créé·e avec succès !')

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
                "Tu ne peux créer qu'un seul personnage.\n"
                "N'hésite pas à taper la commande \"!help creer\" pour avoir "
                "de l'aide.")
        if isinstance(error, CharacterAlreadyExist):
            await context.send(
                "Le personnage que tu souhaites créer existe déjà !")

    @command(name='supprimer', usage='<Prénom> | <Prénom Nom>',
             aliases=['suppr', 'delete', 'del'],
             checks=[no_direct_message, in_command_channel])
    async def delete(self, context: Context, *, name: is_name):
        """
        Supprime un de tes personnages.

        Te permet de supprimer un de tes personnages lié au serveur sur lequel
        tu effectues cette commande. Tu peux avoir jusqu'à 3 personnages.
        """
        author, guild, path, characters = _init_data(context)

        id_ = f'{guild.id}-{author.id}-{name}'
        if id_ not in characters:
            raise UnknownCharacters

        characters.pop(id_)
        leader_flag = False
        for character in characters.values():
            if character.is_leader:
                leader_flag = True
                break
        if not leader_flag and characters:
            list(characters.values())[0].is_leader = True

        store_characters(path, characters)
        await context.send(f'{name} supprimé·e avec succès !')

    @delete.error
    async def delete_error(self, context: Context, error):
        if isinstance(error, BadArgument):
            await context.send("Le format de nom n'est pas bon, désolé.\n"
                               "Test le format de ton nom ici : "
                               f"{NAME_PATTERN_LINK}\n"
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

    @command(name='lister', aliases=['liste', 'list'],
             checks=[no_direct_message, in_command_channel])
    async def list(self, context: Context):
        """
        Liste vos personnages.

        Te permet de supprimer un de tes personnages lié au serveur sur lequel
        tu effectues cette commande. Tu peux avoir jusqu'à 3 personnages.
        """
        author, guild, _, characters = _init_data(context)

        if len(characters) < 1:
            raise NoCharacters
        char_list = ',\n\t'.join(
            character._name for character in characters.values())
        await context.send(f'Voici la liste de tes personnages :\n\t'
                           f'{char_list}.')

    @list.error
    async def list_error(self, context: Context, error):
        if isinstance(error, NoCharacters):
            await context.send(
                "Tu n'a aucun personnage.\n"
                "N'hésite pas à taper la commande \"!help Personnage\" pour "
                "avoir de l'aide.")

    @command(name='fiche', aliases=['profil', 'sheet'],
             checks=[no_direct_message, in_command_channel])
    async def character_sheet(self, context: Context, *,
                              name: Optional[is_name]):
        """
        Fiche du personnage.

        Te permet d'afficher la fiche d'un personnage lié au serveur sur lequel
        tu effectues cette commande.
        """
        author, guild, _, characters = _init_data(context)

        if not name:
            return await context.send(f'', embed=get_leader(characters).embed)

        id_ = f'{guild.id}-{author.id}-{name}'
        if id_ not in characters:
            raise UnknownCharacters
        await context.send(f'', embed=characters[id_].embed)

    @character_sheet.error
    async def character_sheet_error(self, context: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom exact (nom si il y a, aussi) !\n"
                "N'hésite pas à taper la commande \"!help fiche\" pour "
                "avoir de l'aide.")
        if isinstance(error, UnknownCharacters):
            await context.send(
                "Le personnage est introuvable.\n"
                "N'hésite pas à taper la commande \"!help fiche\" pour "
                "avoir de l'aide.")
        if isinstance(error, BadArgument):
            await context.send(
                "Le format de nom n'est pas bon, désolé.\n"
                "Test le format de ton nom ici : "
                f"{NAME_PATTERN_LINK}\n"
                f"N'hésite pas à taper la commande "
                f"\"!help supprimer\" pour avoir de l'aide."
            )

    @command(name='classement', aliases=['leaderboard', 'ranking', 'rank'],
             checks=[no_direct_message, in_command_channel])
    async def leaderboard(self, context: Context, *, type_: Optional[ranking_type] = None):
        if type_ == GLOBAL_RANKING:
            guilds = self.bot.guilds
            await global_leaderboard(context, guilds, context.author)
        else:
            await local_leaderboard(context, context.guild, context.author)

    @leaderboard.error
    async def leaderboard_error(self, context: Context, error):
        if isinstance(error, CommandInvokeError):
            await context.send("Aucun joueurs n'a encore joué, le classement "
                               "n'est donc pas disponible.")
        else:
            raise error

def setup(bot):
    bot.add_cog(Personnage(bot))
