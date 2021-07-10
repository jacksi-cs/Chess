import chess
board = chess.Board()

move = chess.Move.from_uci("a2a4")
board.push(move)
test = board
board.pop()
print(test)