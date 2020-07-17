from discord.ext.commands import Bot, Cog, command, Context

from src.commands.utils import no_direct_message, in_command_channel
from src.constants.INFO import GITHUB_PROJECT
from src.constants.INFORMATIONS import ISSUE_TEMPLATE_TEXT


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

    @command(name='issues', aliases=['issue', 'i'],
             checks=[in_command_channel])
    async def issue(self, context: Context):
        """
        Lien pour demander des fonctionnalités ou remonter des bogues.

        Les modèles d'issues sont traduits. Si vous souhaitez faire votre
        commentaire en français, pensez à sélectionner une issue précédée par
        les lettres "FR", les isntructions sont traduites pour vous aider.
        """
        await context.send(ISSUE_TEMPLATE_TEXT)

def setup(bot):
    bot.add_cog(Informations(bot))
