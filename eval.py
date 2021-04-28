"Contains the evaluation functions and decision making."
def first_move(cboard):
    for i in cboard.legal_moves:
        return i.uci()