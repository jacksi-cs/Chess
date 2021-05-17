"Contains the evaluation functions and decision making."

import chess
import random

# Picks the first move and returns an AN string
def first_move(cboard):
    for i in cboard.legal_moves:
        return cboard.san(i)

def random_move(cboard):
    return cboard.san(random.choice(list(cboard.legal_moves)))