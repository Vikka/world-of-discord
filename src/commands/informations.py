from discord.ext.commands import Bot, Cog, command, Context

from src.commands.utils import no_direct_message, in_command_channel
from src.constants.INFO import GITHUB_PROJECT


class Informations(Cog):
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @command(name='road_map', aliases=['planning'],
             checks=[no_direct_message, in_command_channel])
    async def road_map(self, context: Context):
        await context.channel.send(GITHUB_PROJECT)



def setup(bot):
    bot.add_cog(Informations(bot))
