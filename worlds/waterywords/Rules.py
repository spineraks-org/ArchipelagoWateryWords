import math
from collections import Counter, defaultdict
from typing import List, Optional

from BaseClasses import MultiWorld

from worlds.generic.Rules import set_rule

# This module adds logic to the apworld.
# In short, we ran a simulation for every possible combination of dice and rolls you can have, per category.
# This simulation has a good strategy for locking dice.
# This gives rise to an approximate discrete distribution per category.
# We calculate the distribution of the total score.
# We then pick a correct percentile to reflect the correct score that should be in logic.
# The score is logic is *much* lower than the actual maximum reachable score.

def set_yacht_rules(world: MultiWorld, player: int):
    """
    Sets rules on reaching scores
    """

    for location in world.get_locations(player):
        set_rule(
            location,
            lambda state, curscore=location.watery_words_score, player=player: 
                calculate_score_in_logic(state.count_group("Tiles", player), state.count("Extra turn", player)) >= curscore,
        )
        
def calculate_score_in_logic(letters, turns):
    if letters < 8:
        return letters
    return min(letters * 2.25, turns * 20)


def set_yacht_completion_rules(world: MultiWorld, player: int):
    """
    Sets rules on completion condition
    """
    world.completion_condition[player] = lambda state: state.has("Victory", player)
