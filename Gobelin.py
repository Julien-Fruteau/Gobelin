# TO DO
# Pause to follow combat?
# Print some stats.


#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt

import random
import matplotlib.pyplot as plt
# import numpy as np
from collections import Counter
import pandas as pd
# import scipy.stats as ss


intro = """
---- Introduction -------
Trois gobelins, Grunty, Stinky, et Horrty jouent au jeu (ici revisité)
du combat au Dé Gobelin.

Les règles sont très simples. Chaque gobelin lance un dé, et est
autorisé à frapper avec un gourdin sur la tête d'un autre gobelin,
choisi au hasard, autant de fois que le nombre de points sur son
dé l'indique. Ça s'appelle un dégât.

Chaque gobelin ayant un nombre de points de vie (combien de dégats il
peut encaisser) le dernier gobelin debout sera le vainqueur.

Notez qu'un dé dans une grotte de gobelins est fabriqué en os, et n'a pas
six faces comme le dé que vous pourriez connaître.
Chaque dé a une valeur minimale (nombre de points) et maximale, propre
a chaque gobelin.

Ce jeu n'est jamais vraiment devenu populaire en dehors des sociétés des
grottes gobelines, il se pourrait même que ce soit la raison principale
de l'extinction des gobelins.\n"""


# FUNCTIONS _________________________________________________________________
def create_gobelin(name):
    '''
    Return a list with gobelin name, hitpoints which will evolve in combat,
    min_damage, max_damage, initial hitpoints for later analysis
    '''
    hp = random.choice(range(min_hitpoints, max_hitpoints))
    gobelin = [name,
               hp,
               random.choice(range(min_damage_min, max_damage_min)),
               random.choice(range(min_damage_max, max_damage_max)),
               hp]
    return gobelin


def damage_by(gobelin):
    '''
    Return random damage between min and max damage for a given Gobelin
    '''
    return random.randint(gobelin[2], gobelin[3])


def random_gobelin_hit(gobelins, gobelin):
    """
    Return the index of a random gobelin who's hit by gobelin.

    It is assumed gobelin will not hit itself.
    """
    gobelin_to_hit = list(range(len(gobelins)))
    gobelin_to_hit.remove(gobelin)
    return random.choice(gobelin_to_hit)


def handle_hitpoints(gobelins, gobelin, gobelin_hit, comments):
    '''
    Module to adjust hitpoints of the gobelin_hit by gobelin.

    Since life cannot be negative, adjust to zero if result is negative.

    If gobelin down, remove it from gobelins
    '''
    damage = damage_by(gobelin)
    gobelins[gobelin_hit][1] -= damage

    if gobelins[gobelin_hit][1] < 0:
        gobelins[gobelin_hit][1] = 0

    if comments:
        print("{0} hits {1} for {2} damage. {1} has {3} hp left.".
              format(gobelin[0], gobelins[gobelin_hit][0], damage,
                     gobelins[gobelin_hit][1]))

    if gobelins[gobelin_hit][1] == 0:
        if comments:
            print("{0} falls in combat after {1} rounds".
                  format(gobelins[gobelin_hit][0], combatround))
        gobelins.remove(gobelins[gobelin_hit])


def run_game(comments=False):
    '''
    Return the winner and number of combatround
    '''
    # VARIABLES _____________________________________________________________

    gobelins = [["Stinky", stinky_hitpoints, stinky_min_damage,
                 stinky_max_damage, stinky_hitpoints],
                ["Grunty", grunty_hitpoints, grunty_min_damage,
                 grunty_max_damage, grunty_hitpoints],
                ["Horrty", horrty_hitpoints, horrty_min_damage,
                 horrty_max_damage, horrty_hitpoints]]

    gobelins.append(create_gobelin("Randty"))

    # gobelins = [create_gobelin(name) for name in gobelins_name]

    combatround = 0  # le mot "round" est un mot-cle reserve a Python

    # INIT GAME _____________________________________________________________
    random.shuffle(gobelins)
    if comments:
        print(intro)
        for gobelin in gobelins:
            print("{0} has {1} hitpoints.".format(gobelin[0], gobelin[1]))

    # MAIN LOOP _____________________________________________________________
    while len(gobelins) > 1:
        combatround += 1
        if comments:
            print(" ----- combat round {0} -------".format(combatround))

        for i, gobelin in enumerate(gobelins):

            gobelin_hit = random_gobelin_hit(gobelins, i)

            handle_hitpoints(gobelins, gobelin, gobelin_hit, comments)
    # END GAME ______________________________________________________________
    if comments:
        print("==================================")
        print("The combat ends after %i rounds" % combatround)
        print(gobelins[0][0] + " is the winner !")
    return(gobelins[0][0], gobelins[0][4],
           gobelins[0][2], gobelins[0][3], combatround)


# GLOBALS ___________________________________________________________________
# # définition de Grunty et Stinky. Notez que les variables sont en minuscules
stinky_hitpoints = 50  # Stinky est faible
grunty_hitpoints = 60  # Grunty est fort
horrty_hitpoints = 40

stinky_min_damage = 3  # Stinky fait de meilleurs degats au minimum
stinky_max_damage = 5  # mais pas beaucoup de degats au maximum

grunty_min_damage = 1  # Grunty fait tres peu de degats au minimum
grunty_max_damage = 6  # mais plus de degats au maximum

horrty_min_damage = 2
horrty_max_damage = 5

# Gobelin Population characteristics:
min_hitpoints = 1
max_hitpoints = 101

min_damage_min = 1
max_damage_min = 5

min_damage_max = 5
max_damage_max = 9

# gobelins_name = ["Grunty", "Stinky", "Horrty"]


# ANALYSIS __________________________________________________________________
victories = pd.DataFrame(
    columns=("winner", "hp", "min_dam", "max_dam", "combatround"))

for rep in range(10):
    # (winner, hp, min_dam, max_dam, combatround) = run_game()
    victories.loc[rep + 1] = run_game()


randty_wins = victories[victories.winner == "Randty"]

# shows the frequency of wins for each gobelin
win_freq = Counter(victories.winner)
plt.bar(range(len(win_freq)), win_freq.values())
plt.xticks(range(len(win_freq)), win_freq.keys())
plt.show()

# Rules:
# How many gobelins fight? 4, given 3 gobelins and a random gobelin at each
# game iteration.

# given a gobelin population, which gobelin characteristic will win the most
# and which one will loose the most?

# it is obvious that a gobelin having 100 hp and [4-8] damages will
# win the most.
# hence to deinie a population, we can sample from a normal distribution
# with mean the average of min-max hp/damage_min/damage_max:


# how can the population would mutate towards the most frequent winner?
