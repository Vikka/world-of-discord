from discord.ext.commands import Cog, command, Context


class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='quit', hidden=True)
    async def start(self, context: Context):
        """
        Permet de quitter le bot avec un peu de cleanup.
        """
        ...


def setup(bot):
    bot.add_cog(Admin(bot))
