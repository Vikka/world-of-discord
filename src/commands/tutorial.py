from discord.ext.commands import Cog, Context, command, BadArgument

TUTORIAL_CHAPTER = {
    0: "World of Discord est un MMORPG textuel auquel il est possible de "
       "jouer via discord. \n"
       "\n"
       "Chaque serveur représente une guilde dans le jeu, "
       "ainsi, si tu veux jouer dans une certaine guilde avec tes amis, "
       "n'oublie pas que vous devez, tes amis et toi, avoir un personnage sur "
       "un serveur commun.\n"
       "Tu peux créer des personnages sur autant de serveur que tu le "
       "souhaites.",
    1: "Pour pouvoir jouer à World of Discord, il te faut d'abord créer "
       "un personnage. Pour se faire, il te suffit d'utiliser la "
       "commande `!creer` suivie du prénom de ton personnage (tu peux "
       "préciser un nom de famille si tu le souhaites). Tu peux créer "
       "plusieurs personnages.\n"
       "\n"
       "Ensuite, sache que ton personnage "
       "principal jouera automatiquement pendants 5 minutes lorsque tu es "
       "actif sur le serveur."
}


def check_chapter(chapter: str):
    conversion = 0
    if not chapter.isdigit() or (conversion := int(chapter)) not in (0, 1):
        raise BadArgument
    return conversion


class Tutoriel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='tutoriel', usage='<n° de chapitre>',
             aliases=['tutorial', 'tuto'])
    async def tutorial(self, context: Context, *, chapter: check_chapter = -1):
        """
        Permet de commencer le tutoriel pour jouer.

        Chapitre 1: Créer un personnage pour démarrer l'aventure.
        """
        await context.send(TUTORIAL_CHAPTER[chapter])

    @tutorial.error
    async def tutorial_error(self, context: Context, error: Exception):
        if isinstance(error, BadArgument):
            await context.send("Le format de chapitre n'est pas bon. Soit tu "
                               "ne met rien pour avoir l'introduction, "
                               "soit tu y entre un numéro correspondant aux "
                               "chapitres disponibles.")


def setup(bot):
    bot.add_cog(Tutoriel(bot))
