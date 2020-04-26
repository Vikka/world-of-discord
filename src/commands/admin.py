from discord.ext.commands import Cog, command, Context, Bot

from src.commands.utils import is_admin


class Admin(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(hidden=True, checks=[is_admin])
    async def quit(self, context: Context):
        """
        Permet de quitter le bot avec un peu de cleanup.
        """
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Admin(bot))
