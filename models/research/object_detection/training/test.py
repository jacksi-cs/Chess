from chess_detection_time import func
from stopwatch import Stopwatch, profile
from board import Board
from chess_detection_test import detection
import chess

board = Board(chess.White)

detection(board)