from asyncio import sleep

from discord import Message, Game
from discord.ext.commands import Bot

from src.classes.Character import Character
from src.utils.utils import clear_instances


async def activity(bot: Bot) -> None:
    while True:
        clear_instances(Character)
        print(Character._instances)
        activity_g = Game(f'{len(Character._instances)} active players')
        await bot.change_presence(activity=activity_g)
        await sleep(12)
