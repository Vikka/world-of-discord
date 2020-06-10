from discord import Guild, PermissionOverwrite
from discord.ext.commands import Cog, command, Context, Bot
from discord.utils import get

from src.errors.guild import ChannelAlreadyExist
from src.commands.utils import is_admin, is_owner


class Admin(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @command(checks=[is_admin])
    async def quit(self, _: Context):
        """
        Permet de quitter le bot avec un peu de cleanup.
        """
        await self.bot.logout()

    @command(checks=[is_owner])
    async def install(self, context: Context):
        guild: Guild = context.guild
        if get(guild.channels, name='world of discord'):
            raise ChannelAlreadyExist

        event_permission = {
            guild.default_role: PermissionOverwrite(send_messages=False),
            guild.me: PermissionOverwrite(send_messages=True)
        }
        cat = await guild.create_category('world of discord')
        await guild.create_text_channel('événements', category=cat,
                                        overwrites=event_permission)
        await guild.create_text_channel('commandes', category=cat)


def setup(bot):
    bot.add_cog(Admin(bot))
