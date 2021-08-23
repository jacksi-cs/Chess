"Contains the evaluation functions and decision making."

from re import S
import chess
import random
from anytree import Node, RenderTree
from stopwatch import Stopwatch
import time
from board import Board

counter = 0
recurr_list = {}

piece_value = {
    'P' : 1,
    'N' : 3,
    'B' : 3,
    'R' : 5,
    'Q' : 9,
    'K' : 0.5, # Kings will always be on the board
    'p' : -1,
    'n' : -3,
    'b' : -3,
    'r' : -5,
    'q' : -9,
    'k' : -0.5
}


def recur_func_2(node_info, max_depth, cbrd, eval, depth, alpha, beta): # node_info = [id, parent, move]
    node = Node(name=node_info[0], parent=node_info[1], cboard=cbrd, move=node_info[2], score=None, bmove=None)

    if node.depth == max_depth or not any(cbrd.legal_moves): # Reached max depth, end of game, or leaf node due to truncation
        node.score = eval(node.cboard)
        return node.score, node.move
    else:
        counter = 0

        alpha = float('-inf')
        beta = float('inf')

        "Attempt at removing repetitive game states, but only increased time"
        recurr_list_elem = (cbrd.board_fen(), cbrd.castling_rights, node.depth)
        in_recurr_list = True
        if recurr_list_elem in recurr_list:
            return recurr_list[recurr_list_elem]
        else:
            in_recurr_list = False

        for move in cbrd.legal_moves:
            cbrd.push(move)
            cbrd_modified = cbrd.copy()
            # cbrd_modified = chess.Board(cbrd.fen())
            cbrd.pop()

            eval_score = recur_func_2([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)

            if node.score == None:
                node.score = eval_score[0]
                node.bmove = eval_score[1]
            elif cbrd.turn: # White's turn (max node)
                # alpha beta pruning
                alpha = max(alpha, eval_score[0])
                if beta <= alpha:
                    print("PRUNED")
                    counter += 1
                    break

                if node.score < eval_score[0]:
                    node.score = eval_score[0]
                    node.bmove = eval_score[1]
            else: # Black's turn (min node)
                # alpha beta pruning
                beta = min(beta, eval_score[0])
                if beta <= alpha:
                    print("PRUNED")
                    counter += 1
                    break

                if node.score > eval_score[0]:
                    node.score = eval_score[0]
                    node.bmove = eval_score[1]
            
            counter += 1

        "Attempt at removing repetitive game states, but only increased time"
        if not in_recurr_list:
            recurr_list[recurr_list_elem] = (node.score, node.move)
            
        if node.depth == 0:
            return node.score, node.bmove, node

        return node.score, node.move
        

def minimax_recur(board, eval):
    stopwatch = Stopwatch()
    stopwatch.start()
    global recurr_list
    global counter

    recurr_list = {} # Emptying global cache of board states previously seen, find a better way to design this
    # root = generate_tree(0, None, cboard, None, depth)
    # stopwatch.start()

    # Pass in current cboard which will generate node, look through children, recurse
    test = recur_func_2([0, None, None], board.depth, board.cboard, eval, 0, float('-inf'), float('inf'))
    stopwatch.stop()
    print(str(stopwatch))
    # print(RenderTree(test[2], maxlevel=2))
    print(test[0], test[1])
    return board.cboard.san(test[1])

# Picks the first move and returns an AN string
def first_move(cboard):
    for i in cboard.legal_moves:
        return cboard.san(i)

# Picks a random move
def random_move(cboard):
    return cboard.san(random.choice(list(cboard.legal_moves)))


piece_type_list = [chess.PAWN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.QUEEN, chess.KING]
def eval2(cboard):
    # Determining whether or not checkmate or stalemate
    check = 0
    if cboard.is_checkmate():
        if cboard.turn == chess.WHITE:
            return -100
        elif cboard.turn == chess.BLACK:
            return 100
    if cboard.is_stalemate():
        return 0

    # Small incentive to check the opponent
    if cboard.is_check():
        if cboard.turn == chess.WHITE:
            check = -5
        elif cboard.turn == chess.BLACK:
            check = 5

    bb_white_pieces = chess.SquareSet(chess.BB_ALL)
    for piece_type in piece_type_list:
        bb_white_pieces = bb_white_pieces | cboard.pieces(piece_type, chess.WHITE)

    bb_black_pieces = chess.SquareSet(chess.BB_ALL)
    for piece_type in piece_type_list:
        bb_black_pieces = bb_black_pieces | cboard.pieces(piece_type, chess.BLACK)
    
    ally_multiplier = 1.2
    opponent_multiplier = 1.1

    value = 0

    row = 56
    column = 0
    for char in cboard.board_fen():
        if char != '/':
            if char.isdigit():
                column += int(char)
            else:
                if char.isupper():
                    value += ally_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_white_pieces)))
                    value += opponent_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_black_pieces)))
                elif char.islower():
                    value += ally_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_black_pieces)))
                    value += opponent_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_white_pieces)))

                value += (piece_value[char] * (len(cboard.attacks(row+column) | (~bb_white_pieces & ~bb_black_pieces))))
                column += 1
        else:
            row -= 8
            column = 0

    return value + check

counter=0 
# Naive evaluation function (piece capture, checkmate)
# White trying to maximize, black is trying to minimize
def naive_eval(cboard):
    white_count = 0
    black_count = 0

    global counter
    counter += 1
    if cboard.is_checkmate():
        if cboard.turn == chess.WHITE:
            return -100
        elif cboard.turn == chess.BLACK:
            return 100
    if cboard.is_stalemate():
        return 0

    board_fen = cboard.board_fen()
    for char in board_fen:
        if char.isupper():
            white_count += piece_value[char]
        elif char.islower():
            black_count += piece_value[char]

    return white_count + black_count

# # MAIN
board = Board(chess.WHITE)
board.cboard = chess.Board("r1b1k1nr/1p1p1p2/2n1pqp1/p1b3B1/2B1P2p/2N2N2/PPP2PPP/R2QR1K1 w kq - 0 10")

minimax_recur(board, eval2)