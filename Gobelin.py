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


gobelins = {"Stinky": [stinky_hitpoints, stinky_min_damage,
                       stinky_max_damage],
            "Grunty": [grunty_hitpoints, grunty_min_damage,
                       grunty_max_damage],
            "Horrty": [horrty_hitpoints, horrty_min_damage,
                       horrty_max_damage]}

combatround = 0  # le mot "round" est un mot-cle reserve a Python


def damage_by(gobelin):
    '''
    Return random damage between min and max damage for a given Gobelin
    '''
    return random.randint(gobelins[gobelin][1], gobelins[gobelin][2])


def handle_hitpoints(gobelin_hit, gobelin):
    '''
    Module to adjust hitpoints of the gobelin_hit by gobelin.

    Since life cannot be negative, adjust to zero if result is negative.
    '''
    damage = damage_by(gobelin)
    gobelins[gobelin_hit][0] -= damage

    if gobelins[gobelin_hit][0] < 0:
        gobelins[gobelin_hit][0] = 0

    print("{0} hits {1} for {2} damage. {1} has {3} hp left.".
          format(gobelin, gobelin_hit, damage, gobelins[gobelin_hit][0]))


# def random_gobelin_hit(gobelins, gobelin):
def random_gobelin_hit(gobelins_left, gobelin):
    """
    Return a random gobelin name who's hit by gobelin.

    It is assumed gobelin will not hit itself.

    A gobelin already down is not hit, whereas it might be tempting.

    The function is built to extend at will the list of gobelins beyond 2.
    """
    # beware to make a copy of the list, because see:
    # gobelin_to_hit = gobelins_left
    # gobelin_to_hit is gobelins_left
    # Returns True and mess everything's up...
    gobelin_to_hit = list(gobelins_left)
    gobelin_to_hit.remove(gobelin)
    return random.choice(gobelin_to_hit)


# START _____________________________________________________________________
print(intro)

# define hit gobelin name order list:
gobelins_left = list(gobelins.keys())
# shuffle who hits first and so on:
random.shuffle(gobelins_left)
# present init status of gobelins
for gobelin in gobelins_left:
    print("{0} has {1} hitpoints.".format(gobelin, gobelins[gobelin][0]))

# MAIN LOOP _________________________________________________________________
while len(gobelins_left) > 1:
    combatround += 1
    print(" ----- combat round {0} -------".format(combatround))

    for gobelin in gobelins_left:

        gobelin_hit = random_gobelin_hit(gobelins_left, gobelin)

        handle_hitpoints(gobelin_hit, gobelin)

        if gobelins[gobelin_hit][0] == 0:
            # update list to avoid fallen gobelin to hit anyone :)
            gobelins_left.remove(gobelin_hit)
            print("{0} falls in combat after {1} rounds".
                  format(gobelin_hit, combatround))

# END GAME __________________________________________________________________
print("==================================")
print("The combat ends after %i rounds" % combatround)

for gobelin in gobelins:
    if gobelins[gobelin][0] > 0:
        print(gobelin + " is the winner !")

# Below some tests:
# gobelins.values()
# list(gobelins.values())[1][0]
# list(gobelins.values())[0][0]
# len(list(gobelins.values()))
#
#
# gobelins_left = list(list(gobelins.values())[ind][0] for
#               ind in range(len(list(gobelins.values()))))

# random_gobelin = random.randint(0, 1)
# order = {'Stinky': random_gobelin, 'Grunty': int(not random_gobelin)}
# gobelins_left = [list(order.keys())[list(order.values()).index(ind)]
#                      for ind in sorted(list(order.values()))]


# while stinky_hitpoints > 0 or grunty_hitpoints > 0:

# Loop until at least one of the gobelins has no more hitpoints left.
# while np.all(np.array(list(list(gobelins.values())[ind][0]
#                            for ind in range(len(list(gobelins.values())))))
#              > 0):
