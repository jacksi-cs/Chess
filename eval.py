"Contains the evaluation functions and decision making."

from re import S
import chess
import random
from anytree import Node, RenderTree
from stopwatch import Stopwatch
import time
from board import Board

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
        elif cboard.turn: # White's turn (max node)
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


def recur_func_2(node_info, max_depth, cbrd, eval, depth, alpha, beta): # node_info = [id, parent, move]
    node = Node(name=node_info[0], parent=node_info[1], cboard=cbrd, move=node_info[2], score=None, bmove=None)
    # print(node.depth, node.cboard.turn)

    if node.depth == max_depth or not any(cbrd.legal_moves):
        node.score = eval(node.cboard)
        return node.score, node.move
    else:
        counter = 0
        if cbrd.can_claim_draw():
            print("REEEEEEEEEEEEEEE")

        alpha = float('-inf')
        beta = float('inf')
        for move in cbrd.legal_moves:
            cbrd.push(move)
            cbrd_modified = chess.Board(cbrd.fen())
            cbrd.pop()
            if node.score == None:
                # print("a", node)
                eval_score = recur_func_2([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)
                node.score = eval_score[0]
                node.bmove = eval_score[1]
            elif cbrd.turn: # White's turn (max node)
                eval_score = recur_func_2([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)

                # alpha beta pruning
                # if eval_score[0] != None:
                alpha = max(alpha, eval_score[0])
                if beta <= alpha:
                    print("PLEASE SEE")
                    counter += 1
                    break

                # DEBUG
                # if eval_score[0] == None:
                #     print(eval_score, cbrd_modified, node.depth)
                #     print([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)
                if node.score < eval_score[0]:
                    node.score = eval_score[0]
                    node.bmove = eval_score[1]
            else: # Black's turn (min node)
                eval_score = recur_func_2([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)

                # alpha beta pruning
                # if eval_score[0] != None:
                beta = min(beta, eval_score[0])
                if beta <= alpha:
                    print("PLEASE SEE")
                    counter += 1
                    break


                # DEBUG
                # if eval_score[0] == None:
                #     print(eval_score, cbrd_modified, node.depth)
                #     print([counter, node, move], max_depth, cbrd_modified, eval, depth+1, alpha, beta)
                if node.score > eval_score[0]:
                    node.score = eval_score[0]
                    node.bmove = eval_score[1]
            
            counter += 1
            
        if node.depth == 0:
            return node.score, node.bmove, node


        if node.score == None:
            print(node)
            print("YEH YOH")
        return node.score, node.move
        

def minimax_recur(board, eval):
    stopwatch = Stopwatch()
    stopwatch.start()
    global recurr_list
    global counter

    recurr_list = [] # Emptying global cache of board states previously seen, find a better way to design this
    # root = generate_tree(0, None, cboard, None, depth)
    # stopwatch.start()

    # Pass in current cboard which will generate node, look through children, recurse
    test = recur_func_2([0, None, None], board.depth, board.cboard, eval, 0, float('-inf'), float('inf'))
    stopwatch.stop()
    print(str(stopwatch))
    # print(RenderTree(test[2]))
    print(test[0], test[1])
    return board.cboard.san(test[1])

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

    board_fen = cboard.board_fen()
    for char in board_fen:
        if char.isupper():
            white_count += piece_value[char]
        elif char.islower():
            black_count += piece_value[char]

    return white_count + black_count

# # MAIN
board = Board(chess.WHITE)
board.cboard = chess.Board("rnbqkbnr/pppppppp/6N1/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1")

minimax_recur(board, naive_eval)