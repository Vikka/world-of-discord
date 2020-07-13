from typing import Tuple, Dict

from discord import Member, Guild

from src.classes.Challenger import Challenger
from src.classes.Character import Character, leader_from_author_guild
from src.errors.character import NoLeader
from src.errors.pvp import OnlyOneCharacter


def check_list(waiting_list: Dict[int, Challenger], author: Member,
               guild: Guild) \
        -> Tuple[Challenger, Challenger]:
    leader = leader_from_author_guild(author, guild)

    if author.id in waiting_list.keys():
        raise OnlyOneCharacter(waiting_list[author.id].character._name)

    opponent = waiting_list.popitem()[1]
    return Challenger(leader, author), opponent


def register(waiting_list: Dict[int, Challenger], author: Member,
             leader: Character) -> Dict[int, Challenger]:
    if not leader:
        raise NoLeader

    waiting_list[author.id] = Challenger(leader, author)
    return waiting_list
