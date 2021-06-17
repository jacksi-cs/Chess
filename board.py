"Contains the board class which consists of the board data structure, player side, and tile position for macros."

import chess
import pyautogui
from enum import Enum
import time

array_indexer = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}

# Mouse macro that will alt-tab back into terminal/window
def window_swap():
    print("SWAP")
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

class Board:
    cboard = chess.Board()
    a1_pos = (307, 962)
    jmp_dist = 110

    def __init__(self, side):
        self.side = side # White or black side
        self.init_tiles()

    def init_tiles(self):
        self.tiles = [None] * 64
        
        for i in range(0,8):
            for j in range(0,8):
                self.tiles[i*8+j] = (self.a1_pos[0] + self.jmp_dist * j, self.a1_pos[1] - self.jmp_dist * i)

        if self.side == chess.BLACK:
            self.tiles.reverse()

    def move(self, move, swap):
        if swap:
            window_swap()
        self.macro_move(self.cboard.parse_san(move).uci())
        self.cboard.push_san(move)


    # Takes in a UCI string (how I implemented it before, so didn't want to change it)
    def macro_move(self, move):
        if self.side == self.cboard.turn:
            print("The program has decided on the move: ", move)
            source = self.tiles[(int(move[1]) - 1) * 8 + array_indexer[move[0]]] # ex. e2e4
            destination = self.tiles[(int(move[3]) - 1) * 8 + array_indexer[move[2]]]
            pyautogui.click(source)
            pyautogui.click(destination)

