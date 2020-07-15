import re
from typing import Optional

from discord.ext.commands import Cog, Context, command, BadArgument, \
    MissingRequiredArgument, Bot, CommandInvokeError

from src.classes.Character import Character, get_path_and_characters, \
    store_characters, get_leader
from src.commands.utils import no_direct_message, in_command_channel
from src.constants.CONSTANTS import DEFAULT_VALUE, VALUE, GUILDS_RANKING, \
    EXP_VALUE
from src.constants.CONSTANTS import RANKING, DEFAULT_RANKING
from src.constants.REGEX import NAME_PATTERN, NAME_PATTERN_LINK
from src.errors.character import TwoManyCharacters, UnknownCharacters, \
    NoCharacters, CharacterAlreadyExist
from src.manipulation.context_manipulation import get_author_guild_from_context
from src.manipulation.leaderboard.leaderboard import leaderboard_embed

name_pattern = re.compile(NAME_PATTERN, flags=re.I)


def is_name(name: str) -> str:
    """For command annotation"""
    if not name:
        return ''
    if not name_pattern.match(name):
        raise BadArgument
    return name.lower().title()


def check_ranking_type(ranking_type: str) -> str:
    """For command annotation"""
    if ranking_type not in RANKING:
        print(ranking_type)
        raise BadArgument
    return ranking_type.lower()


def check_value_type(value_type: str) -> str:
    """For command annotation"""
    if value_type not in VALUE:
        print(value_type)
        raise BadArgument
    return value_type.lower()


def _init_data(context: Context):
    author, guild = get_author_guild_from_context(context)
    path, characters = get_path_and_characters(author, guild)
    return author, guild, path, characters


class Personnage(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command(name='creer', usage='[<Prénom>|<Prénom Nom>]',
             aliases=['créer', 'create', 'new'],
             checks=[no_direct_message, in_command_channel])
    async def create(self, context: Context, *, name: is_name):
        """
        Enregistre un nouveau personnage.

        Te permet de créer un personnage lié au serveur sur lequel tu
        effectues cette commande. Tu peux créer jusqu'à 1 personnages.

        Attention, la taille du nom et du prénom doit être comprise entre
        2 et 15 caractères.

        Exemples (penses à ajouter le préfixe de commande !):
            créer Leroy
            create Leroy Jenkins
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
        help_quote = "N'hésite pas à taper la commande \"!help creer\" pour " \
                     "avoir de l'aide."
        if isinstance(error, BadArgument):
            await context.send("Le format de nom n'est pas bon, désolé.\n"
                               "Test le format de ton nom ici : "
                               "https://regex101.com/r/GWsaBf/2\n"
                               f"{help_quote}")
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom (tu peux aussi préciser le nom) !\n"
                f"{help_quote}")
        if isinstance(error, TwoManyCharacters):
            await context.send(
                "Tu ne peux créer qu'un seul personnage.\n"
                f"{help_quote}")
        if isinstance(error, CharacterAlreadyExist):
            await context.send(
                "Le personnage que tu souhaites créer existe déjà !")

    @command(name='supprimer', usage='[<Prénom>|<Prénom Nom>]',
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
        help_quote = "N'hésite pas à taper la commande \"!help " \
                     "[supprimer|suppr|delete|del]\" pour avoir de l'aide."
        if isinstance(error, BadArgument):
            await context.send("Le format de nom n'est pas bon, désolé.\n"
                               "Test le format de ton nom ici : "
                               f"{NAME_PATTERN_LINK}\n"
                               f"{help_quote}")
        if isinstance(error, UnknownCharacters):
            await context.send(
                "Le personnage est introuvable.\n"
                f"{help_quote}")
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom exact (nom si il y a, aussi) !\n"
                f"{help_quote}")

    @command(name='lister', aliases=['liste', 'list', 'personnages'],
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
                "N'hésite pas à taper la commande \"!help "
                "[lister|liste|list|personnages]\" pour avoir de l'aide.")

    @command(name='fiche', aliases=['profil', 'sheet', 'personnage', 'perso'],
             checks=[no_direct_message, in_command_channel])
    async def character_sheet(self, context: Context, *,
                              name: Optional[is_name] = None):
        """
        Fiche du personnage.

        Te permet d'afficher la fiche d'un personnage lié au serveur sur lequel
        tu effectues cette commande.

        Exemples (penses à ajouter le préfixe de commande !):
            fiche
            profil Leroy
            personnage Leroy Jenkins
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
        help_quote = "N'hésite pas à taper la commande \"!help " \
                     "[fiche|profil|sheet|personnage|perso]\" pour avoir de " \
                     "l'aide."
        if isinstance(error, MissingRequiredArgument):
            await context.send(
                "Tu as oublié le prénom exact (nom si il y a, aussi) !\n"
                f"{help_quote}")
        if isinstance(error, UnknownCharacters):
            await context.send(
                "Le personnage est introuvable.\n"
                f"{help_quote}")
        if isinstance(error, BadArgument):
            await context.send(
                "Le format de nom n'est pas bon, désolé.\n"
                "Test le format de ton nom ici : "
                f"{NAME_PATTERN_LINK}\n"
                f"{help_quote}"
            )

    @command(name='classement',
             aliases=['leaderboard', 'ranking', 'rank', 'c', 'r'],
             checks=[no_direct_message, in_command_channel],
             usage='[membres(par défaut)|guildes] [niveaux(par défaut)|'
                   'expérience|puissance|tués|rares|duels]')
    async def leaderboard(self, context: Context,
                          ranking_type: check_ranking_type = DEFAULT_RANKING,
                          value_type: check_value_type = DEFAULT_VALUE):
        """
        Affiche le classement des joueurs ou des guildes.

        Par défaut, le classement est celui des joueurs, mais tu peux préciser
        le type avec le premier argument. Voici les possibilités :
            - 'membres', 'membre', 'members', 'member', 'm',
            - 'guildes', 'guilde', 'guilds', 'guild', 'g'.

        Par défaut, la valeur utilisée pour classer est le niveau, mais tu peux
        préciser cette valeur avec le second argument. Voici les possibilités :
            - 'niveaux', 'level', 'niv', 'lvl', 'n', 'l',
            - 'expérience', 'experience', 'exp', 'xp', 'e', 'x',
            - 'puissance', 'power', 'pow', 'p',
            - 'tués', 'kills', 't', 'k',
            - 'rares', 'rare', 'r',
            - 'duels', 'duel', 'dudu', 'd'.

        Exemples (penses à ajouter le préfixe de commande !):
            classement
            classement guildes duels
            ranking members exp
            c g niv
            r m p
        """
        print(ranking_type)
        data = self.bot.guilds \
            if ranking_type in GUILDS_RANKING \
            else context.guild
        await context.send(embed=leaderboard_embed(data,
                                                   context.author,
                                                   ranking_type,
                                                   value_type))

    @leaderboard.error
    async def leaderboard_error(self, context: Context, error):
        if isinstance(error, CommandInvokeError):
            await context.send("Aucun joueurs n'a encore joué, le classement "
                               "n'est donc pas disponible.")
            raise error
        else:
            raise error


def setup(bot):
    bot.add_cog(Personnage(bot))
