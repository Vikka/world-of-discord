import re
from random import randint
from os import listdir
from os.path import isfile, join

from discord import TextChannel, Message, File
from discord.ext import commands
from discord.ext.commands import Cog, Context

from src.classes.Item import Item
from src.constants.PATH import ITEM_NAME_PATH

loot = re.compile(r'!item')
item_name = re.compile(r'([a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂ'
                       r'ÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ._\s-]{5,60})')

ASSETS = 'assets/icon_pack/Weapons'


async def loot_help(channel: TextChannel):
    msg = "HELP: !item"
    return await channel.send(msg)


async def name_item_help(channel: TextChannel):
    msg = "HELP: !name_item <Nom de l'objet>"
    return await channel.send(msg)


class Debug(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def generate_image(self, context: Context):
        """
        Only for Server owner.
        """
        channel: TextChannel = context.channel
        if channel.name != 'bricabot':
            return
        only_files = [f for f in listdir(ASSETS) if isfile(join(ASSETS, f))]
        for file_name in only_files:
            file = File(f'{ASSETS}/{file_name}', filename=file_name)
            result = await context.channel.send(file_name, file=file)
            with open('data/item_links/weapons_url', 'a') as weapons_url:
                weapons_url.write(f'{result.attachments[0].url}\n')

    @commands.command(hidden=True)
    async def item(self, context: Context):
        """
        Channel loots. Command : !item

        Exemple d'utilisation : !item
        """
        await context.send(embed=Item(randint(1, 10)).embed)


def setup(bot):
    bot.add_cog(Debug(bot))
