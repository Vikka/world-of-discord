from __future__ import annotations

from math import floor
from random import choices
from typing import Dict, Literal, Callable, Coroutine, Any, Tuple, Union

from discord import Reaction, Message, Emoji, DMChannel, TextChannel

from src.classes.Challenger import Challenger
from src.classes.Character import Character
from src.constants.EMOJIS import EMOJI_ATTACK, EMOJI_DEFENSE, EMOJI_FEINT, \
    EMOJI_NAME_ATTACK, EMOJI_NAME_DEFENSE, EMOJI_NAME_FEINT
from src.constants.JSON_KEY import ELO, PVP1V1_TOTAL_GAMES, PVP1V1_TOTAL_LOSE, \
    PVP1V1_TOTAL_WIN
from src.constants.PVP import ATTACK, DEFENSE, FEINT
from src.utils.utils import first

WIN = "Tu gagnes !"
LOSE = "Tu perds !"


class Player:
    power: int
    _life: int
    cooldown: int
    debuff: int
    action: int

    def __init__(self, power, life, cooldown, debuff, action):
        self.power = power
        self._life = life
        self.cooldown = cooldown
        self.debuff = debuff
        self.action = action

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = floor(value)


def minus_life(defender, attacker) -> Tuple[int, bool]:
    defender -= floor(attacker)
    return defender, defender > 0


class PVP1V1:
    switch = Dict[int, Challenger]
    first_player: Literal[-1, 1]
    player_1: Challenger
    player_2: Challenger
    p1_stats: Player
    p2_stats: Player
    turn: Literal[0, 1]
    set_action_switch: Dict[str, Callable[[DMChannel],
                                          Coroutine[Any, Any, None]]]
    action_switch: Dict[int, Callable[[...], Tuple[str, str]]]
    origin_channel: TextChannel

    def __init__(self,
                 switch: Dict[int, Challenger],
                 first_player: Literal[-1, 1],
                 player_1: Challenger,
                 player_2: Challenger,
                 origin_channel: TextChannel):
        self.switch = switch
        self.first_player = first_player
        self.player_1 = player_1
        self.player_2 = player_2
        self.origin_channel = origin_channel
        self.turn = 0
        self.set_action_switch = {
            EMOJI_NAME_ATTACK: self.set_attack,
            EMOJI_NAME_DEFENSE: self.set_defense,
            EMOJI_NAME_FEINT: self.set_feint,
        }
        self.action_switch = {
            1: self.attack,
            2: self.defense,
            3: self.feint,
        }

        p1_stats = Player(
            player_1.character.pvp_power,
            player_1.character.pvp_life,
            0,
            0,
            None,
        )

        p2_stats = Player(
            player_2.character.pvp_power,
            player_2.character.pvp_life,
            0,
            0,
            None,
        )
        self.player_stat = {
            -1: p1_stats,
            1: p2_stats,
        }

    async def react(self, reaction: Reaction, fight_list: Dict[int, PVP1V1]) \
            -> Union[int, Tuple[Character, Character]]:
        message: Message = reaction.message
        emoji: Emoji = reaction.emoji
        new = False

        await self.set_action_switch.get(emoji.name)(message.channel)

        # Message de fin de tour
        # Code

        if self.turn:
            self.turn = 0

            # first to play
            attacker = self.switch.get(self.first_player)
            defender = self.switch.get(-self.first_player)
            att_stat = self.player_stat.get(self.first_player)
            def_stat = self.player_stat.get(-self.first_player)

            att_msg = f"Ton adversaire a répliqué.\n"
            def_msg = f"Ton adversaire t'attaque.\n"
            att_tmp, def_tmp = self.action_switch.get(att_stat.action)(
                att_stat, def_stat)
            att_msg += att_tmp
            def_msg += def_tmp
            await attacker.member.send(att_msg)
            await defender.member.send(def_msg)
            new = True
        else:
            self.turn += 1
        if not new:
            if (
                    actual := self.player_stat.get(
                        -self.first_player)).cooldown == 0:
                self.first_player *= -1
            else:
                actual.cooldown -= 1
                self.turn += 1

        else:
            self.first_player = choices(
                (-1, 1),
                (self.player_1.character.pvp_power,
                 self.player_2.character.pvp_power)
            ).pop()
            if (
                    actual := self.player_stat.get(
                        self.first_player)).cooldown != 0:
                self.first_player *= -1
                actual.cooldown -= 1
                self.turn += 1

        # DEAD Resolve
        i_dead: int = first(self.player_stat, lambda x: self.player_stat[x].life <= 0)
        if i_dead is not None:
            dead: Character = self.switch.get(i_dead).character
            vict: Character = self.switch.get(-i_dead).character
            dead.increment_stat(PVP1V1_TOTAL_GAMES)
            dead.increment_stat(PVP1V1_TOTAL_LOSE)
            vict.increment_stat(PVP1V1_TOTAL_GAMES)
            vict.increment_stat(PVP1V1_TOTAL_WIN)
            return dead, vict

        message: Message = await self.switch.get(self.first_player) \
            .member.send("A vous de jouer")
        fight_list[message.id] = self
        await self.add_combat_reaction(message)
        return 0

    async def set_attack(self, channel: DMChannel):
        attacker = self.player_stat.get(self.first_player)
        attacker.action = ATTACK
        await channel.send(f'Tu attaques !')

    async def set_defense(self, channel: DMChannel):
        attacker = self.player_stat.get(self.first_player)
        attacker.action = DEFENSE
        await channel.send(f'Tu te défends !')

    async def set_feint(self, channel: DMChannel):
        attacker = self.player_stat.get(self.first_player)
        attacker.action = FEINT
        await channel.send(f'Tu fais une feinte !')

    @staticmethod
    def attack(att_stat: Player, def_stat: Player):
        def_action = def_stat.action
        att_stat.action = 0
        def_stat.action = 0
        if def_action == 1:
            att_stat.life, alive = minus_life(att_stat.life, def_stat.power)
            if not alive:
                return LOSE, WIN
            def_stat.life, alive = minus_life(def_stat.life, att_stat.power)
            if not alive:
                return WIN, LOSE
            return ("Il t'attaque aussi.\n"
                    f"Tu perds {def_stat.power} points de vie.\n"
                    f"Lui perd {att_stat.power} points de vie.",
                    "Il t'attaque aussi.\n"
                    f"Tu perds {att_stat.power} points de vie.\n"
                    f"Lui perd {def_stat.power} points de vie.")

        if def_action == 2:
            att_stat.cooldown = 2
            return ("Il bloque complètement ton attaque et te déstabilise "
                    "pendant deux tours !",
                    "Ton adversaire attaque alors que tu t'y attendais, "
                    "tu ne subit pas de perte de point de vie et retarde sa "
                    "prochaine action de deux tours !")
        if def_action == 3:
            att_stat.life, alive = minus_life(att_stat.life,
                                              def_stat.power * .2)
            if not alive:
                return LOSE, WIN
            def_stat.life, alive = minus_life(def_stat.life, att_stat.power)
            if not alive:
                return WIN, LOSE
            return ("Il tente une feinte, mais ton attaque le surprends.\n"
                    f"Tu perds {floor(def_stat.power * .2)} points de vie.\n"
                    f"Lui perd {att_stat.power} points de vie.",
                    "Ton adversaire attaque alors que tu préparais une "
                    "feinte ! Il te surprends et tu ne lui inflige que "
                    f"{floor(def_stat.power * .2)} dégats, tandis que tu perds "
                    f"{att_stat.power} points de vie.")
        def_stat.life, alive = minus_life(def_stat.life, att_stat.power)
        if not alive:
            return WIN, LOSE
        return ("Ton adversaire est encore déstabilisé, ton coup touche et "
                f"lui fait perdre {att_stat.power} points de vie",
                "Tu es encore déstabilité, et ton adversaire frappe.\n"
                f"Tu perds {att_stat.power} points de vie.")

    @staticmethod
    def defense(att_stat: Player, def_stat: Player):
        def_action = def_stat.action
        att_stat.action = 0
        def_stat.action = 0
        if def_action == 1:
            def_stat.cooldown = 2
            return ("Ton adversaire attaque alors que tu t'y attendais, "
                    "tu ne subit pas de perte de point de vie et retarde sa "
                    "prochaine action de deux tours !",
                    "Il bloque complètement ton attaque et te déstabilise "
                    "pendant deux tours !")
        if def_action == 2:
            return ("Vous êtes tout les deux sur la défensive, attendant le "
                    "bon moment pour frapper.",
                    "Vous êtes tout les deux sur la défensive, attendant le "
                    "bon moment pour frapper.")
        if def_action == 3:
            att_stat.life, alive = minus_life(att_stat.life,
                                              def_stat.power * .5)
            if not alive:
                return LOSE, WIN
            att_stat.cooldown = 1
            return ("Tu es sur la défensive, mais ton adversaire te feinte et"
                    f" pénètre ta défense ! Tu perds {floor(att_stat.power * .5)} "
                    f"points de vie et tu es déstabilisé pendant un tour !",
                    "Votre adversaire est sur la défensive mais votre feinte "
                    "vous permet de pénètrer ses défenses. Vous lui infligez "
                    f"{floor(att_stat.power * 0.5)} dégats et le déstabilisez un "
                    f"tour !")
        return ("Ton adversaire est encore déstabilisé, tu a été "
                "inutilement prudent !",
                "Tu es encore déstabilisé, mais ton adversaire s'est trop "
                "méfié ! Il ne t'a donc pas attaqué !")

    @staticmethod
    def feint(att_stat: Player, def_stat: Player):
        def_action = def_stat.action
        att_stat.action = 0
        def_stat.action = 0
        if def_action == 1:
            att_stat.life, alive = minus_life(att_stat.life, def_stat.power)
            if not alive:
                return LOSE, WIN
            def_stat.life, alive = minus_life(def_stat.life,
                                              att_stat.power * .2)
            if not alive:
                return WIN, LOSE
            return ("Ton adversaire attaque alors que tu préparais une "
                    "feinte ! Il te surprends et tu ne lui inflige que "
                    f"{floor(att_stat.power * 0.2)} dégats, tandis que tu perds "
                    f"{def_stat.power} points de vie.",
                    "Il tente une feinte, mais ton attaque le surprends.\n"
                    f"Tu perds {floor(def_stat.power * .2)} points de vie.\n"
                    f"Lui perd {att_stat.power} points de vie.")
        if def_action == 2:
            def_stat.life, alive = minus_life(def_stat.life,
                                              att_stat.power * .5)
            if not alive:
                return WIN, LOSE
            def_stat.cooldown = 1
            return ("Votre adversaire est sur la défensive mais votre feinte "
                    "vous permet de pénètrer ses défenses. Vous lui infligez "
                    f"{floor(att_stat.power * 0.5)} dégats et le déstabilisez un "
                    f"tour !",
                    "Tu es sur la défensive, mais ton adversaire te feinte et"
                    f" pénètre ta défense ! Tu perds {floor(att_stat.power * .5)} "
                    f"points de vie et tu es déstabilisé pendant un tour !")
        if def_action == 3:
            att_stat.life, alive = minus_life(att_stat.life,
                                              def_stat.power * .2)
            if not alive:
                return LOSE, WIN
            def_stat.life, alive = minus_life(def_stat.life,
                                              att_stat.power * .2)
            if not alive:
                return WIN, LOSE
            return ("Vous tentez tout les deux une feinte, ce qui vous "
                    "perturbe.\n"
                    f"Tu perds {floor(def_stat.power * .2)} points de vie.\n"
                    f"Lui perd {floor(att_stat.power * .2)} points de vie.",
                    "Vous tentez tout les deux une feinte, ce qui vous "
                    "perturbe.\n"
                    f"Tu perds {floor(att_stat.power * .2)} points de vie.\n"
                    f"Lui perd {floor(def_stat.power * .2)} points de vie.")
        def_stat.life, alive = minus_life(def_stat.life, att_stat.power * .5)
        if not alive:
            return WIN, LOSE
        return ("Ton adversaire est encore déstabilisé, ta feinte est inutile "
                "et n'a fait qu'affaiblir ton coup.\n"
                f"Tu ne lui inflige que {floor(att_stat.power * .5)} points de vie.",
                "Tu es encore déstabilisé, mais ton adversaire à tout de même "
                "fait une feinte, ce qui à affaiblie la force de son coup !\n"
                f"Tu ne perds que {floor(att_stat.power * .5)} points de vie.")

    @staticmethod
    async def add_combat_reaction(message):
        await message.add_reaction(EMOJI_ATTACK)
        await message.add_reaction(EMOJI_DEFENSE)
        await message.add_reaction(EMOJI_FEINT)
