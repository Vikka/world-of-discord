import os

from discord.ext.commands import Cog, Context, command, BadArgument
from dotenv import load_dotenv

from src.errors.tutorial import WrongChapter
from src.commands.utils import in_command_channel

load_dotenv()
ADD_BOT = os.getenv('ADD_BOT')
SUMMARY = "Liste des chapitres:\n" \
          "\tChapitre -1 : Installation du jeu sur un serveur.\n" \
          "\tChapitre 0 : Présentation du jeu.\n" \
          "\tChapitre 1 : Créer un personnage pour démarrer l'aventure."

TUTORIAL_CHAPTER = {
    -1: "Chapitre -1\n"
        "Configuration :\n"
        f"- {ADD_BOT}\n"
        "- Permettre au bot de lire tous les channels, et ce pour s'assurer "
        "que tous les joueurs puissent jouer correctement (le bot lit les "
        "messages pour activer les combats automatiquement,\n"
        "- Lancer la commande '!install' pour installer automatiquement les "
        "prérequis au fonctionnement du bot suivants :\n"
        "\t- Créer une catégorie 'World of Discord', seule catégorie où le bot "
        "sera habilité à écrire,\n"
        "\t- Créer un channel 'événements' où le bot pourra communiquer les "
        "news du serveur et autres événements,\n"
        "\t- Créer un channel 'commandes', seul endroit où les commandes du "
        "jeu pourront être écrites. Aucun autre bot ne devrait pouvoir lire ce "
        "channel, afin d'éviter tout conflit de commande.",
    0: "Chapitre 0\n"
       "World of Discord est un MMORPG textuel auquel il est possible de "
       "jouer via discord. \n"
       "\n"
       "Chaque serveur représente une guilde dans le jeu, "
       "ainsi, si tu veux jouer dans une certaine guilde avec tes amis, "
       "n'oublie pas que vous devez, tes amis et toi, avoir un personnage sur "
       "un serveur commun.\n"
       "Tu peux créer des personnages sur autant de serveur que tu le "
       "souhaites.\n\n"
       f"{SUMMARY}",
    1: "Chapitre 1\n"
       "Pour pouvoir jouer à World of Discord, il te faut d'abord créer "
       "un personnage. Pour se faire, il te suffit d'utiliser la "
       "commande `!creer` suivie du prénom de ton personnage (tu peux "
       "préciser un nom de famille si tu le souhaites). Tu peux créer "
       "plusieurs personnages.\n"
       "\n"
       "Ensuite, sache que ton personnage "
       "principal jouera automatiquement pendants 5 minutes lorsque tu es "
       "actif sur le serveur.\n\n"
       f"{SUMMARY}"
}


def check_chapter(chapter: str) -> int:
    try:
        chapter = int(chapter)
    except ValueError:
        raise BadArgument
    if chapter not in TUTORIAL_CHAPTER:
        raise WrongChapter
    return chapter


class Tutoriel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='tutoriel', usage='<n° de chapitre(0 par défaut)>',
             aliases=['tutorial', 'tuto'], checks=[in_command_channel])
    async def tutorial(self, context: Context, *, chapter: check_chapter = 0):
        f"""
        Permet de commencer le tutoriel pour jouer.

        {SUMMARY}
        """
        await context.send(TUTORIAL_CHAPTER[chapter])

    @tutorial.error
    async def tutorial_error(self, context: Context, error: Exception):
        if isinstance(error, BadArgument):
            await context.send("Le format de chapitre n'est pas bon. Soit tu "
                               "ne met rien pour avoir l'introduction, "
                               "soit tu y entre un numéro correspondant aux "
                               "chapitres disponibles.")
        if isinstance(error, WrongChapter):
            await context.send("Le chapitre que tu souhaites consulter "
                               "n'existe pas.")


def setup(bot):
    bot.add_cog(Tutoriel(bot))
