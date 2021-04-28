"Contains the evaluation functions and decision making."

import chess

def first_move(cboard):
    for i in cboard.legal_moves:
        return cboard.san(i)