import re

from discord import Guild, Embed
from discord.ext.commands import Cog, Context, command, BadArgument, \
    MissingRequiredArgument, Bot

from errors.character import TwoManyCharacters, UnknownCharacters, \
    NoCharacters, CharacterAlreadyExist
from src.classes.Character import Character
from src.commands.utils import no_direct_message, in_command_channel
from src.constants.CONSTANTS import RANKING, GLOBAL_RANKING, DEFAULT_RANKING
from src.constants.REGEX import NAME_PATTERN, NAME_PATTERN_LINK
from src.manipulation.character_manipulation import _get_path_and_characters, \
    _store_characters
from src.manipulation.context_manipulation import get_author_guild_from_context

name_pattern = re.compile(NAME_PATTERN, flags=re.I)


def is_name(name: str):
    """For command annotation"""
    if not name_pattern.match(name):
        raise BadArgument
    return name


def ranking_type(type_: str):
    """For command annotation"""
    if not type_:
        return DEFAULT_RANKING
    if type_ not in RANKING:
        raise BadArgument
    return type_


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

    @command(name='supprimer', usage='<Prénom> | <Prénom Nom>',
             aliases=['suppr', 'delete', 'del'],
             checks=[no_direct_message, in_command_channel])
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
        author, guild = get_author_guild_from_context(context)
        _, characters = _get_path_and_characters(author, guild)

        if len(characters) < 1:
            raise NoCharacters

        char_list = ',\n\t'.join(character for character in characters.keys())
        await context.send(f'Voici la liste de tes personnages :\n\t'
                           f'{char_list}.')

    @list.error
    async def list_error(self, context: Context, error):
        if isinstance(error, NoCharacters):
            await context.send(
                "Tu n'a aucun personnage.\n"
                "N'hésite pas à taper la commande \"!help Personnage\" pour "
                "avoir de l'aide.")

    @command(name='fiche', aliases=['sheet'],
             checks=[no_direct_message, in_command_channel])
    async def character_sheet(self, context: Context, *, name: is_name):
        """
        Fiche du personnage.

        Te permet d'afficher la fiche d'un te des personnage lié au serveur sur
        lequel tu effectues cette commande.
        """
        author, guild = get_author_guild_from_context(context)
        _, characters = _get_path_and_characters(author, guild)

        if name not in characters:
            raise UnknownCharacters

        await context.send(f'', embed=characters[name].embed)

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

    @command(name='classement', aliases=['leaderboard'], hidden=True,
             checks=[no_direct_message, in_command_channel])
    async def leaderboard(self, context: Context, *, type_:ranking_type):
        if type_ == GLOBAL_RANKING:
            if not self.bot.guilds:
                return
            guild_list = list()
            for guild in self.bot.guilds:
                max_exp = 0
                for member in guild.members:
                    path, characters = _get_path_and_characters(member, guild)
                    tmp_exp = 0
                    for character in characters.values():
                        if character.total_exp > tmp_exp:
                            tmp_exp = character.total_exp
                    if tmp_exp > max_exp:
                        max_exp = tmp_exp
                guild_list.append((guild.name, max_exp))
            guild_list.sort(key=lambda x: x[1], reverse=True)
            embed = Embed(title='Classement des Guildes')
            embed.add_field(name='n°', value=str(1))
            embed.add_field(name='Nom', value=guild_list[0][0])
            embed.add_field(name='Exp max', value=guild_list[0][1])
            names = tuple()
            values = tuple()
            for i, guild in enumerate(guild_list, start=1):
                if i % 2 != 0:
                    names = (str(i), guild[0], guild[1])
                else:
                    values = (str(i), guild[0], guild[1])
                    embed.add_field(name=names[0], value=values[0])
                    embed.add_field(name=names[1], value=values[1])
                    embed.add_field(name=names[2], value=values[2])
                    values = 0
            if values == 0:
                embed.add_field(name=str(len(guild_list)), value='\u200b')
                embed.add_field(name=guild_list[-1][0], value='\u200b')
                embed.add_field(name=guild_list[-1][1], value='\u200b')
            await context.send(embed=embed)

        ...


def setup(bot):
    bot.add_cog(Personnage(bot))
