from re import S
import chess
import random
from anytree import Node, RenderTree
from stopwatch import Stopwatch
import time


generate_avg = [0,0]
push_avg = [0,0]
pop_avg = [0,0]
recurr_list = []
counter = 0
noncounter = 0
def generate_tree(id, prnt, cbrd, mv, depth):
    stopwatch = Stopwatch()
    global generate_avg
    global push_avg
    global pop_avg

    global counter
    global noncounter

    global recurr_list

    if depth >= 0:
        counter += 1
        stopwatch.start()
        node = Node(id, parent = prnt, cboard=cbrd, move=mv, score=None, bmove=None) # identification, parent of the node, cboard of the node, move of the node, score of the node, best move of its children
        id = 0
        # print("generate: ", str(stopwatch))
        for move in cbrd.legal_moves:
            stime = time.time()
            # stopwatch.restart()
            cbrd.push(move)
            # print("push: ", stopwatch)
            # etime = time.time()
            # push_avg[0] += etime-stime
            # push_avg[1] += 1
            if (cbrd.board_fen(),cbrd.castling_rights) not in recurr_list:
                generate_tree(id, node, chess.Board(cbrd.fen()), move, depth-1)
                recurr_list.append((cbrd.board_fen(),cbrd.castling_rights))
            else:
                noncounter += 1
            # stime = time.time()
            # stopwatch.restart()
            cbrd.pop()
            # print("pop: ", str(stopwatch))
            # etime = time.time()
            # pop_avg[0] += etime-stime
            # pop_avg[1] += 1
            id += 1

        if (prnt == None):
            counter += 1
            return node

cboard = chess.Board("rnbqkbnr/pppppppp/7N/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1")
stopwatch = Stopwatch()
stopwatch.start()
root = generate_tree(0, None, cboard, None, 4)
stopwatch.stop()
print(str(stopwatch), counter, noncounter, len(root.leaves))
# print("generate: ", generate_avg[0]/generate_avg[1], "push: ", push_avg[0]/push_avg[1], "pop: ", pop_avg[0]/pop_avg[1])
# print(RenderTree(root))