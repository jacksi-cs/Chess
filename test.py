import chess
board = chess.Board("rnbqkb1r/pp1pnppp/2pN4/4p3/8/7N/PPPPPPPP/R1BQKB1R b KQkq - 3 4")

for move in board.legal_moves:
    print(move)
# print(test)
# board.pop()
# print(test)