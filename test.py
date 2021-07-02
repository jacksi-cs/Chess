from chess_detection_time import func
from stopwatch import Stopwatch, profile
from board import Board
import chess

board = Board(chess.White)

while True:
    stopwatch = Stopwatch()
    stopwatch.start()
    func()
    stopwatch.stop()
    print("3 ", stopwatch.elapsed)