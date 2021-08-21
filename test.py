import chess

board = chess.Board()

board.push(chess.Move.from_uci('e2e4'))
test = board.copy()
print(test)
board.pop()
print(test)