"Contains the evaluation functions and decision making."

from re import S
import chess
import random
from anytree import Node, RenderTree
from stopwatch import Stopwatch
import time

counter = 0
recurr_list = []

piece_value = {
    'P' : 1,
    'N' : 3,
    'B' : 3,
    'R' : 5,
    'Q' : 9,
    'K' : 0, # Kings will always be on the board
    'p' : -1,
    'n' : -3,
    'b' : -3,
    'r' : -5,
    'q' : -9,
    'k' : 0
}

# Constructs game tree recursively; could improve time with 1D or bitboard representation
generate_avg = [0,0]
push_avg = [0,0]
pop_avg = [0,0]
def generate_tree(id, prnt, cbrd, mv, depth):
    
    global generate_avg
    global push_avg
    global pop_avg

    global counter
    global recurr_list

    if depth >= 0:
        counter += 1
        stime = time.time()
        node = Node(id, parent = prnt, cboard=cbrd, move=mv, score=None, bmove=None) # identification, parent of the node, cboard of the node, move of the node, score of the node, best move of its children
        id = 0
        etime = time.time()
        generate_avg[0] += etime-stime
        generate_avg[1] += 1
        for move in cbrd.legal_moves:
            stime = time.time()
            cbrd.push(move)
            etime = time.time()
            push_avg[0] += etime-stime
            push_avg[1] += 1
            if (cbrd.board_fen(),cbrd.castling_rights) not in recurr_list:
                generate_tree(id, node, chess.Board(cbrd.fen()), move, depth-1)
                recurr_list.append((cbrd.board_fen(),cbrd.castling_rights))
            stime = time.time()
            cbrd.pop()
            etime = time.time()
            pop_avg[0] += etime-stime
            pop_avg[1] += 1
            id += 1

        if (prnt == None):
            return node

def recur_func(cboard, eval, node, turn, alpha, beta):
    if node.is_leaf:
        node.score = eval(node.cboard)
        return node.score, node.move
    
    for child in node.children:
        if node.score == None:
            eval_score = recur_func(cboard, eval, child, not turn, alpha, beta)
            node.score = eval_score[0]
            node.bmove = eval_score[1]
        elif turn: # White's turn (max node)
            eval_score = recur_func(cboard, eval, child, not turn, alpha, beta)

            # alpha beta pruning
            alpha = max(alpha, eval_score[0])
            if beta <= alpha:
                break

            if node.score < eval_score[0]:
                node.score = eval_score[0]
                node.bmove = eval_score[1]
        else: # Black's turn (min node)
            eval_score = recur_func(cboard, eval, child, not turn, alpha, beta)

            # alpha beta pruning
            beta = min(beta, eval_score[0])
            if beta <= alpha:
                break

            if node.score > eval_score[0]:
                node.score = eval_score[0]
                node.bmove = eval_score[1]

    return node.score, node.move

def minimax_recur(cboard, eval, depth):
    stopwatch = Stopwatch()
    stopwatch.start()
    global recurr_list
    global counter

    global generate_avg
    global pop_avg
    global push_avg

    recurr_list = [] # Emptying global cache of board states previously seen, find a better way to design this
    root = generate_tree(0, None, cboard, None, depth)
    stopwatch.stop()
    print(str(stopwatch))
    stopwatch.start()
    # print(root, root.cboard, root.is_leaf)
    recur_func(cboard, eval, root, cboard.turn, float('-inf'), float('inf'))
    stopwatch.stop()
    print(root.bmove, counter, str(stopwatch))
    print("generate: ", generate_avg[0]/generate_avg[1], "push: ", push_avg[0]/push_avg[1], "pop: ", pop_avg[0]/pop_avg[1])
    return cboard.san(root.bmove)

# Picks the first move and returns an AN string
def first_move(cboard):
    for i in cboard.legal_moves:
        return cboard.san(i)

# Picks a random move
def random_move(cboard):
    return cboard.san(random.choice(list(cboard.legal_moves)))


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
    if cboard.is_check():
        if cboard.turn == chess.WHITE:
            black_count += -5
        elif cboard.turn == chess.BLACK:
            white_count += 5

    board_fen = cboard.board_fen()
    for char in board_fen:
        if char.isupper():
            white_count += piece_value[char]
        elif char.islower():
            black_count += piece_value[char]

    return white_count + black_count

# # MAIN
board = chess.Board("rnb1qr1k/6bp/2p3pn/pp1pp3/5p1P/5N2/PPPPPPP1/RNBQKB1R w Q - 2 21")
board = chess.Board("rnbqkbnr/pppppppp/7N/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1")

minimax_recur(board, naive_eval, 3)