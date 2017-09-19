# TO DO
# Pause to follow combat?
# Print some stats.


#       Copyright 2011 Horst JENS <horst.jens@spielend-programmieren.at>
#       part of http://ThePythonGameBook.com
#       licence: gpl, see http://www.gnu.org/licenses/gpl-3.0.txt

import random
import matplotlib.pyplot as plt
import numpy as np
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
    Return a list with:
    gobelin name,
    init hitpoints,
    hp left which will evolve in combat,
    min_damage, max_damage,
    mean_dam_given, mean_dam_taken,
    total_dam_given, total_dam_taken, hit_position.
    '''
    hp = random.randint(min_hitpoints, max_hitpoints)
    gobelin = [name,
               hp,
               hp,
               random.randint(min_damage_min, max_damage_min),
               random.randint(min_damage_max, max_damage_max),
               0, 0, 0, 0, 0]
    return gobelin


def init_gobelin(gobelin):
    gobelin[2] = gobelin[1]
    gobelin[5] = 0
    gobelin[6] = 0
    gobelin[7] = 0
    gobelin[8] = 0
    gobelin[9] = 0


def damage_by(gobelin):
    '''
    Return random damage between min and max damage for a given Gobelin
    '''
    return random.randint(gobelin[3], gobelin[4])


def random_gobelin_hit(gobelins, gobelin):
    """
    Return the index of a random gobelin who's hit by gobelin.

    It is assumed gobelin will not hit itself.
    """
    gobelin_to_hit = list(range(len(gobelins)))
    gobelin_to_hit.remove(gobelin)
    return random.choice(gobelin_to_hit)


def handle_hitpoints(gobelins, gobelin, gobelin_hit_id, combatround, comments):
    '''
    Module to adjust hitpoints of the gobelin_hit by gobelin.

    Since life cannot be negative, adjust to zero if result is negative.

    If gobelin down, remove it from gobelins list
    '''
    damage = damage_by(gobelin)
    gobelins[gobelin_hit_id][2] -= damage

    # updates damage tracking:

    # mean_dam_given => updated in the end

    # mean_dam_taken (nb, this is temporary computing, in the end it will
    # computed to the actual mean, using total damage taken [8] and this [6],
    # which is temporarely the frequency at which the gobelin has been hit):
    gobelins[gobelin_hit_id][6] += 1

    # total_dam_given
    gobelin[7] += damage
    # total_dam_taken
    gobelins[gobelin_hit_id][8] += damage

    if gobelins[gobelin_hit_id][2] < 0:
        gobelins[gobelin_hit_id][2] = 0

    if comments:
        print("{0} hits {1} for {2} damage. {1} has {3} hp left.".
              format(gobelin[0], gobelins[gobelin_hit_id][0], damage,
                     gobelins[gobelin_hit_id][2]))

    if gobelins[gobelin_hit_id][2] == 0:
        if comments:
            print("{0} falls in combat after {1} rounds".
                  format(gobelins[gobelin_hit_id][0], combatround))
        gobelins.remove(gobelins[gobelin_hit_id])


def run_game(Randty, comments=False):
    '''
    Return the winner and number of combatround
    '''
    # VARIABLES _____________________________________________________________

    # each gobelin has :
    #      "name", "hp0", "min_dam",
    #      "max_dam", "hp_left,"
    #      "mean_dam_given", "mean_dam_taken",
    #      "total_dam_given", "total_dam_taken,
    #      "hit_position"

    gobelins = [["Stinky",
                 stinky_hitpoints,
                 stinky_hitpoints,
                 stinky_min_damage,
                 stinky_max_damage,
                 0, 0, 0, 0, 0],

                ["Grunty",
                 grunty_hitpoints,
                 grunty_hitpoints,
                 grunty_min_damage,
                 grunty_max_damage,
                 0, 0, 0, 0, 0],

                ["Horrty",
                 horrty_hitpoints,
                 horrty_hitpoints,
                 horrty_min_damage,
                 horrty_max_damage,
                 0, 0, 0, 0, 0]]

    #  Does the random gobelins has to be randomly created at each
    # game iteration. Not sure, let's pass Randy as a param of run_game instead:
    # gobelins.append(create_gobelin("Randty"))
    init_gobelin(Randty)
    gobelins.append(Randty)

    # gobelins = [create_gobelin(name) for name in gobelins_name]

    combatround = 0  # le mot "round" est un mot-cle reserve a Python

    # INIT GAME _____________________________________________________________
    random.shuffle(gobelins)
    if comments:
        print(intro)
        for gobelin in gobelins:
            print("{0} has {1} hitpoints.".format(gobelin[0], gobelin[1]))
    for i, gobelin in enumerate(gobelins):
        gobelin[9] = i + 1

    total_players = len(gobelins)

    # MAIN LOOP _____________________________________________________________
    while len(gobelins) > 1:
        combatround += 1
        if comments:
            print(" ----- combat round {0} -------".format(combatround))

        for i, gobelin in enumerate(gobelins):

            gobelin_hit = random_gobelin_hit(gobelins, i)

            handle_hitpoints(gobelins, gobelin, gobelin_hit,
                             combatround, comments)
    # END GAME ______________________________________________________________
    if comments:
        print("==================================")
        print("The combat ends after %i rounds" % combatround)
        print(gobelins[0][0] + " is the winner !")

    # mean_dam_given by winner:
    gobelin[5] = gobelin[7] / combatround
    # mean_dam_taken by winner:
    gobelin[6] = gobelin[8] / gobelin[6]  # (seen handle_hitpoints())

    return(gobelins[0][0], gobelins[0][1], gobelins[0][2],
           gobelins[0][3], gobelins[0][4],
           gobelins[0][5], gobelins[0][6],
           gobelins[0][7], gobelins[0][8],
           combatround, gobelins[0][9], total_players)


# GLOBALS ___________________________________________________________________
# # définition de Grunty, Stinky, Horrty.
# # Notez que les variables sont en minuscules
stinky_hitpoints = 50  # Stinky est faible
grunty_hitpoints = 60  # Grunty est fort
horrty_hitpoints = 40

stinky_min_damage = 3  # Stinky fait de meilleurs degats au minimum
stinky_max_damage = 5  # mais pas beaucoup de degats au maximum

grunty_min_damage = 1  # Grunty fait tres peu de degats au minimum
grunty_max_damage = 6  # mais plus de degats au maximum

horrty_min_damage = 2
horrty_max_damage = 5

# Gobelin Population characteristics to be chosen randomly from by
# create_gobelin():
min_hitpoints = 1
max_hitpoints = 101

min_damage_min = 1
max_damage_min = 5

min_damage_max = 5
max_damage_max = 9

# gobelins_name = ["Grunty", "Stinky", "Horrty"]


# ANALYSIS __________________________________________________________________


# means = np.empty((0, 2))

# victories = pd.DataFrame(
# columns=("winner", "hp", "min_dam", "max_dam", "combatround"))

victories = pd.DataFrame(
    columns=("winner", "hp", "hp_left",
             "min_dam", "max_dam",
             "mean_dam_given", "mean_dam_taken",
             "total_dam_given", "total_dam_taken",
             "combatround", "hit_position", "total_players"))

# here you can create loop (with below nested loop)
Ranty = create_gobelin("Randty")

# how does the random gobelin Randty performs in X games?:
for rep in range(10):
    victories.loc[rep + 1] = run_game(Ranty)
    # randty_wins = victories[victories.winner == "Randty"]
    # hp_mean = randty_wins.hp.mean()
    # damage_mean = (randty_wins.min_dam.mean() +
    #                randty_wins.max_dam.mean()) / 2
    # means = np.concatenate(
    #     (means, np.array([[hp_mean, damage_mean]])), axis=0)

# Check victorires:
victories.head()
# Check our random gobelin Randty:
Ranty
randty_wins = victories[victories.winner == "Randty"]
randty_wins


# randty_wins.head()

# # shows the frequency of wins for each gobelin
# win_freq = Counter(victories.winner)
# win_freq
# plt.bar(range(len(win_freq)), win_freq.values())
# plt.xticks(range(len(win_freq)), win_freq.keys())
# plt.show()

# display the characteristics of randty, for all his wins
# plt.plot(randty_wins.hp, randty_wins.min_dam, 'ro')
# plt.plot(randty_wins.hp, randty_wins.max_dam, 'bo')
# plt.show()

# # over rep increasing to high number, are randty carac trending towards
# # certain carac?
# plt.figure()
# plt.plot(means[:, 0], 'ro')
# plt.plot(means[:, 1], 'bo')
# plt.show()
