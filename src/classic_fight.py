from asyncio import sleep
from time import time, strftime
from typing import Tuple, Dict

from discord import Member, Guild, Message, TextChannel
from discord.utils import get

from errors.character import NoCharacters, NoLeader, CharactersLocked
from src.classes.Character import Character, get_enemy_life, get_loot
from src.constants.CHANNELS import CHANNEL_INFO_WOD
from src.constants.FIGHT import ATTACK_SPEED, ROUND_TIME
from src.manipulation.character_manipulation import get_leader, \
    _store_characters, _get_path_and_characters


def _init_fight_data(message: Message) -> Tuple[Member, Guild, TextChannel]:
    author: Member = message.author
    guild: Guild = message.guild
    channel: TextChannel = get(guild.channels, name=CHANNEL_INFO_WOD)
    if not channel:
        print(f'ERROR: no {CHANNEL_INFO_WOD} channel.')
    return author, guild, channel


async def init_fight(author: Member, guild: Guild) \
        -> Tuple[Character, str, dict]:
    path, characters = _get_path_and_characters(author, guild)
    if not characters:
        raise NoCharacters

    leader: Character = get_leader(characters)

    if not leader:
        raise NoLeader

    if leader.lock > time():
        leader.lock = int(time()) + ROUND_TIME
        _store_characters(path, characters)
        raise CharactersLocked
    return leader, path, characters


async def fight(fighter: Character, channel: TextChannel, author: Member,
                path: str, characters: Dict[str, Character]):
    print('fight')
    fighter.lock = int(time()) + ROUND_TIME
    _store_characters(path, characters)
    life = get_enemy_life(fighter._level)
    current = life
    next_hit = 0
    print(f'{strftime("%D")}{author.display_name} hit')
    print(f'{time() < fighter.lock}, {time()}, {int(fighter.lock)}')
    while time() < fighter.lock:
        if next_hit >= time():
            await sleep(ATTACK_SPEED/12)
            continue
        print(
            f'{strftime("%X")} {author.display_name} hit for {fighter.power} damages, {current - fighter.power} remaining.')
        if (last := current - fighter.power) > 0:
            current = last
        else:
            current = life
            await get_loot(fighter, channel)
            if fighter.gain_xp(life) and channel:
                await channel.send(
                    f"{fighter._name} vient d'atteindre le niveau "
                    f"{fighter._level} !",
                    embed=fighter.embed)
            _store_characters(path, characters)
        next_hit = time() + ATTACK_SPEED


async def start_classic_fight(message: Message) -> None:
    author, guild, channel = _init_fight_data(message)

    leader, path, characters = await init_fight(author, guild)
    if not (leader and path and characters):
        return
    await fight(leader, channel, author, path, characters)
