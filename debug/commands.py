import re
from random import randint
from os import listdir
from os.path import isfile, join

from discord import TextChannel, Message, File
from discord.ext import commands
from discord.ext.commands import Cog, Context

from src.classes.Item import Item

loot = re.compile(r'!item')
item_name = re.compile(r'!name_item ([a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂ'
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
        with open('data/items_name') as items_name:
            self.names = items_name.read().splitlines()
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
            with open('data/items/weapons_url', 'a') as weapons_url:
                weapons_url.write(f'{result.attachments[0].url}\n')

    @commands.command(hidden=True)
    async def item(self, context: Context):
        """
        Channel loots. Command : !item

        Exemple d'utilisation : !item
        """
        channel: TextChannel = context.channel
        message: Message = context.message
        match = loot.match(message.content)
        if not match:
            return await loot_help(channel)
        await context.send(embed=Item(randint(1, 10)).embed)

    @commands.command(hidden=True)
    async def name_item(self, context: Context, *commands: str):
        """
        Channel name_item. Command : !name_item <Nom de l'objet>

        Exemple d'utilisation : !name_item Deuillelombre
        """
        channel: TextChannel = context.channel

        message: Message = context.message
        match = item_name.match(message.content)
        if not match:
            return await name_item_help(channel)

        if match.group(1).lower() in self.names:
            return await context.send(
                'Le nom existe déjà :) Mais merci de votre participation !')

        with open('data/items_name', 'a') as items_name:
            items_name.write(f'{match.group(1).lower()}\n')
        await context.send('Merci pour votre participation !')


def setup(bot):
    bot.add_cog(Debug(bot))
