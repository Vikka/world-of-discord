from asyncio import sleep
from random import choice

from discord import Guild, PermissionOverwrite
from discord.ext.commands import Cog, command, Context, Bot
from discord.utils import get

from src.errors.guild import ChannelAlreadyExist
from src.commands.utils import is_admin, is_owner
from src.manipulation.leaderboard.local_leaderboard import get_max_xp


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

    @command(checks=[is_admin])
    async def giveaway(self, context: Context, *, msg):
        members = list()
        for member in context.guild.members:
            if (max_xp := get_max_xp(member)) > 0:
                members.append((member.name, max_xp))
        winner = choice(members)[0]
        await context.send(f'La grande loterie va bientôt commencer !!!\n'
                           f'Installez vous, prenez des sucreries, nous allons'
                           f' bientôt tirer au sort le grand gagnant !')
        await sleep(10)
        await context.send(f'Le tirage au sort va être lancé dans 10...')
        await sleep(1)
        for i in range(9, 0, -1):
            await context.send(f'{i}...')
            await sleep(1)
        await context.send(f'NOUS AVONS UN GAGNANT !!!!!!!!!')
        await sleep(5)
        await context.send(f'Le gagnant de la loterie est .....')
        await sleep(2)
        await context.send(f"{winner.capitalize()} !!!!!!!!!!!!")
        await sleep(1)
        await context.send(f'{winner} remporte donc {msg}!!!!')

def setup(bot):
    bot.add_cog(Admin(bot))
