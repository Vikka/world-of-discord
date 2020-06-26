# bot.py
import os
from asyncio import sleep

from discord import Message, DMChannel, Game, Status
from discord.ext.commands import Bot
from dotenv import load_dotenv

# this specifies what extensions to load when the bot starts up
from src.classes.Character import Character, clear_character_instances
from src.classic_fight import start_classic_fight

startup_extensions = ['src.commands.tutorial', 'src.commands.character',
                      'src.commands.admin', 'src.commands.informations']

load_dotenv()

if os.getenv('DEBUG') == 'True':
    startup_extensions.append("src.debug.commands")

COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


class CustomBot(Bot):
    maintenance: True


bot: CustomBot = CustomBot(command_prefix=COMMAND_PREFIX, case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected')
    while True:
        clear_character_instances(Character)
        print(Character._instances)
        activity = Game(f'{len(Character._instances)} active players')
        await bot.change_presence(activity=activity)
        await sleep(12)


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
            or message.author == bot.user
            or isinstance(message.channel, DMChannel))


@bot.event
async def on_message(message: Message):
    await bot.process_commands(message)

    if await stop_trigger(message):
        return

    await start_classic_fight(message)


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
