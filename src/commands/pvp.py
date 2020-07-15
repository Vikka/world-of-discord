from random import choices
from typing import Dict, Literal

from discord import Message
from discord.ext.commands import Cog, Bot, command, Context, CommandInvokeError

from src.classes.Challenger import Challenger
from src.classes.Character import leader_from_author_guild
from src.classes.PVP1V1 import PVP1V1
from src.commands.utils import no_direct_message, in_command_channel
from src.constants.EMOJIS import EMOJI_ATTACK, EMOJI_DEFENSE, EMOJI_FEINT
from src.constants.PVP import REGISTERED, INIT, DM_REGISTERED
from src.duel import register, check_list
from src.errors.pvp import OnlyOneCharacter


class PVP(Cog):
    bot: Bot
    waiting_list: Dict[int, Challenger]
    fight_list: Dict[int, PVP1V1]

    def __init__(self, bot):
        self.bot = bot
        self.waiting_list = dict()
        self.fight_list = dict()

    @command(name='duel', checks=[no_direct_message, in_command_channel],
             hidden=True)
    async def pvp_1v1(self, context: Context):
        """
        Permet d'entrer en lice pour un duel.

        Lorsque vous entrez en duel avec quelqu'un, vous pouvez à nouveau vous
        inscrire avec un de vos personnages, le même si vous le souhaitez.
        Pour cela, il suffit de refaire la commande sur le serveur en question.
        Pour le moment, cependant, ce n'est pas conseillé, car vous risquez de
        vous perdre entre les combats si vous ne faites pas attention ou si
        vous en avez trop.

        ! Cette fonctionnalité est en développement, il y a des bugs, veuillez
        les remonter si ils n'apparaissent pas dans la liste ci-dessous :
            - Lorsque l'ennemi est étourdit, il est possible que le bot ne
            prenne pas votre action en compte. Vous ne verrez donc pas de
            message indiquant qu'il y a eu un affrontement. Vous n'avez qu'a
            appuyer à nouveau sur l'action qui n'a pas été prise en compte pour
            que ça fonctionne.
        """
        if not self.waiting_list:
            author = context.author
            leader = leader_from_author_guild(author, context.guild)

            await author.send(DM_REGISTERED.format(leader._name))

            self.waiting_list = register(self.waiting_list, author, leader)
            await context.send(REGISTERED.format(leader._name))
            return
        player_1, player_2 = check_list(self.waiting_list,
                                        context.author,
                                        context.guild)
        await context.send(f'Duel lancé entre {player_1.character._name} et '
                           f'{player_2.character._name} !')

        switch = {
            -1: player_1,
            1: player_2,
        }
        first_player: Literal[-1, 1] = choices(
            (-1, 1),
            (player_1.character.power, player_2.character.power)
        ).pop()

        message: Message = await switch[first_player].member.send(INIT)
        self.fight_list[message.id] = PVP1V1(switch, first_player,
                                             player_1, player_2,
                                             context.channel)
        await PVP1V1.add_combat_reaction(message)

    @pvp_1v1.error
    async def pvp_1v1_error(self, context: Context, error):
        if isinstance(error, OnlyOneCharacter):
            await context.send(f'Tu es déjà en lice avec {error}')
        if isinstance(error, CommandInvokeError):
            await context.send(f"Tu ne peux pas participer aux duels car tu "
                               f"n'acceptes pas les mp de la part des membres "
                               f"de ce serveur.")
            raise error
        else:
            raise error


def setup(bot):
    bot.add_cog(PVP(bot))
