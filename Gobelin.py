# TO DO
# Pause to follow combat?
# Print some stats.


#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt

import random


intro = """
---- Introduction -------
Trois gobelins, Grunty, Stinky, et Horrty jouent au jeu revisité
du combat au Dé Gobelin.

Les règles sont très simples. Chaque gobelin lance un dé, et est
autorisé à frapper un autre gobelin sur la t’ête avec un gourdin
autant de fois que le nombre de points sur son dé l'indique. Ça
s'appelle un dégât.

Chaque gobelin ayant un nombre de points de vie (combien de dégats il
peut encaisser) le dernier gobelin debout sera le vainqueur.

Notez qu'un dé dans une grotte de gobelins est fabriqué en os, et n'a pas
six faces comme le dé que vous pourriez connaître.
Chaque dé a une valeur minimale (nombre de points) et maximale.

Ce jeu n'est jamais vraiment devenu populaire en dehors des sociétés dans
les grottes gobelines, il se pourrait même que ce soit la raison principale
de l'extinction des gobelins.\n"""


# définition de Grunty et Stinky. Notez que les variables sont en minuscules
stinky_hitpoints = 50  # Stinky est faible
grunty_hitpoints = 60  # Grunty est fort
horrty_hitpoints = 40

stinky_min_damage = 3  # Stinky fait de meilleurs degats au minimum
stinky_max_damage = 5  # mais pas beaucoup de degats au maximum

grunty_min_damage = 1  # Grunty fait tres peu de degats au minimum
grunty_max_damage = 6  # mais plus de degats au maximum

horrty_min_damage = 2
horrty_max_damage = 5

gobelins = [["Stinky", stinky_hitpoints, stinky_min_damage,
             stinky_max_damage],
            ["Grunty", grunty_hitpoints, grunty_min_damage,
             grunty_max_damage],
            ["Horrty", horrty_hitpoints, horrty_min_damage,
             horrty_max_damage]]


combatround = 0  # le mot "round" est un mot-cle reserve a Python


def damage_by(gobelin):
    '''
    Return random damage between min and max damage for a given Gobelin
    '''
    return random.randint(gobelin[2], gobelin[3])


def handle_hitpoints(gobelins, gobelin, gobelin_hit):
    '''
    Module to adjust hitpoints of the gobelin_hit by gobelin.

    Since life cannot be negative, adjust to zero if result is negative.

    If gbelin down, remove it from gobelins
    '''
    damage = damage_by(gobelin)
    gobelins[gobelin_hit][1] -= damage

    if gobelins[gobelin_hit][1] < 0:
        gobelins[gobelin_hit][1] = 0

    print("{0} hits {1} for {2} damage. {1} has {3} hp left.".
          format(gobelin[0], gobelins[gobelin_hit][0], damage,
                 gobelins[gobelin_hit][1]))

    if gobelins[gobelin_hit][1] == 0:
        print("{0} falls in combat after {1} rounds".
              format(gobelins[gobelin_hit][0], combatround))
        gobelins.remove(gobelins[gobelin_hit])


def random_gobelin_hit(gobelins, gobelin):
    """
    Return the index of a random gobelin who's hit by gobelin.

    It is assumed gobelin will not hit itself.
    """
    gobelin_to_hit = list(range(len(gobelins)))
    gobelin_to_hit.remove(gobelin)
    return random.choice(gobelin_to_hit)


# START _____________________________________________________________________
print(intro)

random.shuffle(gobelins)
for gobelin in gobelins:
    print("{0} has {1} hitpoints.".format(gobelin[0], gobelin[1]))

# MAIN LOOP _________________________________________________________________
while len(gobelins) > 1:
    combatround += 1
    print(" ----- combat round {0} -------".format(combatround))

    for i, gobelin in enumerate(gobelins):

        gobelin_hit = random_gobelin_hit(gobelins, i)

        handle_hitpoints(gobelins, gobelin, gobelin_hit)
# END GAME __________________________________________________________________
print("==================================")
print("The combat ends after %i rounds" % combatround)
print(gobelins[0][0] + " is the winner !")
