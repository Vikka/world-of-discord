from discord.ext.commands import Bot, Cog, command, Context

from src.commands.utils import no_direct_message, in_command_channel
from src.constants.INFO import GITHUB_PROJECT
from src.constants.INFORMATIONS import ENHANCEMENT_LIST_TEXT, BUG_LIST_TEXT


class Informations(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command(name='road_map', aliases=['planning', 'road'],
             checks=[no_direct_message, in_command_channel])
    async def road_map(self, context: Context):
        """
        Affiche un lien vers la fiche de route du projet.
        """
        await context.channel.send(GITHUB_PROJECT)

    @command(name='bogues', aliases=['bogue', 'bug', 'issues', 'issue', 'b',
                                     'i'],
             checks=[in_command_channel])
    async def issue(self, context: Context):
        """
        Lien pour consulter/contribuer à la liste des bogues.
        """
        await context.send(BUG_LIST_TEXT)

    @command(name='améliorations', aliases=['amélioration', 'enhancements',
                                            'enhancement', 'a', 'e'],
             checks=[in_command_channel])
    async def enhancement(self, context: Context):
        """
        Lien pour consulter/contribuer à la liste des améliorations.
        """
        await context.send(ENHANCEMENT_LIST_TEXT)


def setup(bot):
    bot.add_cog(Informations(bot))
