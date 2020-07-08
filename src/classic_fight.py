from asyncio import sleep
from datetime import datetime
from time import time, strftime
from typing import Tuple, Dict

from discord import Member, Guild, Message, TextChannel
from discord.utils import get

from src.classes.Character import Character, get_enemy_life, get_loot
from src.constants.CHANNELS import CHANNEL_INFO_WOD
from src.constants.FIGHT import ATTACK_SPEED
from src.errors.character import NoLeader, CharactersLocked
from src.manipulation.character_manipulation import get_leader, \
    store_characters, get_path_and_characters


def _init_fight_data(message: Message) -> Tuple[Member, Guild, TextChannel]:
    author: Member = message.author
    guild: Guild = message.guild
    channel: TextChannel = get(guild.channels, name=CHANNEL_INFO_WOD)
    if not channel:
        print(f'ERROR: no {CHANNEL_INFO_WOD} channel.')
    return author, guild, channel


async def init_fight(author: Member, guild: Guild) \
        -> Tuple[Character, str, dict]:
    path, characters = get_path_and_characters(author, guild)
    leader: Character = get_leader(characters)

    if not leader:
        raise NoLeader

    if leader.lock > time():
        leader.update_lock()
        store_characters(path, characters)
        raise CharactersLocked(datetime.fromtimestamp(leader.lock)
                               .strftime('%H:%M:%S'))
    return leader, path, characters


async def kill_log(loot, level_up, channel, fighter):
    if loot:
        await channel.send(loot[0], embed=loot[1])
    if level_up:
        await channel.send(
            f"{fighter._name} vient d'atteindre le niveau "
            f"{fighter._level} !",
            embed=fighter.embed)


async def killed(fighter, channel, path, characters):
    current = get_enemy_life(fighter._level)
    loot = get_loot(fighter, channel)
    level_up = fighter.gain_xp(current)

    fighter.kills += 1

    if channel:
        await kill_log(loot, level_up, channel, fighter)

    store_characters(path, characters)
    return current


async def hit(current, author, fighter, channel, path, characters):
    print(f'{strftime("%X")} {author.display_name} hit for {fighter.power}'
          f' damages, {current - fighter.power} remaining.')

    return await killed(fighter, channel, path, characters) \
        if (last := current - fighter.power) <= 0 \
        else last


async def fight(fighter: Character, channel: TextChannel, author: Member,
                path: str, characters: Dict[str, Character]):
    print('fight')
    fighter.update_lock()
    store_characters(path, characters)
    current = get_enemy_life(fighter._level)
    print(f'{strftime("%D")}{author.display_name} hit')
    print(f'{time() < fighter.lock}, {time()}, {int(fighter.lock)}')
    while time() < fighter.lock:
        current = await hit(current, author, fighter, channel, path,
                            characters)
        await sleep(ATTACK_SPEED)


async def start_classic_fight(message: Message) -> None:
    author, guild, channel = _init_fight_data(message)

    leader, path, characters = await init_fight(author, guild)
    if not (leader and path and characters):
        return
    await fight(leader, channel, author, path, characters)
