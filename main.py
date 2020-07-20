import os
import re
from asyncio import sleep, gather
from pathlib import Path
from typing import Dict

from discord import Message, DMChannel, Game, Reaction, User
from discord.ext.commands import Bot
from dotenv import load_dotenv

from src.classes.Character import Character, store_characters
from src.classes.PVP1V1 import PVP1V1
from src.classic_fight import start_classic_fight
from src.elo.elo import compute_new_elo
from src.utils.utils import clear_instances
from src.coroutines.activity import activity

startup_extensions = ['src.commands.tutorial', 'src.commands.character',
                      'src.commands.admin', 'src.commands.informations',
                      'src.commands.pvp']

load_dotenv()

if os.getenv('DEBUG') == 'True':
    startup_extensions.append("src.debug.commands")

COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

REG = re.compile(r'([0-9]+)-([0-9]+)-.+')


class CustomBot(Bot):
    maintenance: bool
    command_runing: list

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.command_runing = list()


bot: CustomBot = CustomBot(command_prefix=COMMAND_PREFIX,
                           case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected')
    await gather(activity(bot))


async def stop_trigger(message):
    """
    Stop the event if:
        content starts with '!',
        if the author is the bot,
        if it's a DM Channel,
    :param message:
    :return:
    """
    return (message.content.startswith(COMMAND_PREFIX)
            or message.author.bot
            or isinstance(message.channel, DMChannel))


@bot.event
async def on_message(message: Message):
    await bot.process_commands(message)

    if await stop_trigger(message):
        return

    await start_classic_fight(message)


@bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user.bot:
        return

    message_id = reaction.message.id
    fight_list: Dict[int, PVP1V1] = bot.get_cog('PVP').fight_list

    if fight := fight_list.pop(message_id, None):
        await fight.react(reaction, fight_list)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
