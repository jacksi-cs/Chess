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
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

class Board:
    cboard = chess.Board()

    # Computer on edge
    # detection_dim = (169, 284, 822, 822) # top, left, width, height

    # PVP against friend on edge
    detection_dim = (169,278,835,835)

    def __init__(self, side):
        self.side = side # White or black side
        self.init_lists()

    def init_lists(self):
        "Values based on the actual mouse distance/coordinates on the screen"
        a1_pos = (307, 962)
        jmp_dist = 110

        # PVP against friend/edge
        a1_pos = (331,964)
        jmp_dist = 104

        # Generating tiles (mapping of boxes for mouse macros)
        self.tiles = [None] * 64
        
        for i in range(0,8):
            for j in range(0,8):
                self.tiles[i*8+j] = (a1_pos[0] + jmp_dist * j, a1_pos[1] - jmp_dist * i)

        # Generating board_list (mapping of boxes for detection) and piece_list (list of pieces from a1,..,a8,b1,..,etc)
        self.board_list = []
        self.piece_list = []

        x = [int(self.detection_dim[2]/16 + i*self.detection_dim[2]/8) for i in range(0,8)] # From a to h
        y = [int(self.detection_dim[3]/16 + i*self.detection_dim[3]/8) for i in range(0,8)][::-1] # From 1 to 8

        for x_coord in x:
            for y_coord in y:
                piece_id = None
                x_index = x.index(x_coord)
                y_index = y.index(y_coord)
                if x_index == 0 or x_index == 7:
                    if y_index == 0:
                        piece_id = 7.0 # White rook
                    elif y_index == 7:
                        piece_id = 1.0 # Black rook
                    elif y_index == 1:
                        piece_id = 12.0 # White pawn
                    elif y_index == 6:
                        piece_id = 6.0 # Black pawn
                elif x_index == 1 or x_index == 6:
                    if y_index == 0:
                        piece_id = 8.0 # White knight
                    elif y_index == 7:
                        piece_id = 2.0 # Black knight
                    elif y_index == 1:
                        piece_id = 12.0
                    elif y_index == 6:
                        piece_id = 6.0
                elif x_index == 2 or x_index == 5:
                    if y_index == 0:
                        piece_id = 9.0 # White bishop
                    elif y_index == 7:
                        piece_id = 3.0 # Black bishop
                    elif y_index == 1:
                        piece_id = 12.0
                    elif y_index == 6:
                        piece_id = 6.0
                elif x_index == 3:
                    if y_index == 0:
                        piece_id = 10.0 # White queen
                    elif y_index == 7:
                        piece_id = 4.0 # Black queen
                    elif y_index == 1:
                        piece_id = 12.0
                    elif y_index == 6:
                        piece_id = 6.0
                elif x_index == 4:
                    if y_index == 0:
                        piece_id = 11.0 # White king
                    elif y_index == 7:
                        piece_id = 5.0 # Black king
                    elif y_index == 1:
                        piece_id = 12.0
                    elif y_index == 6:
                        piece_id = 6.0
                self.board_list.append((x_coord, y_coord))
                self.piece_list.append(piece_id)
        
        # Generating cypher_list (list identifying what index represents what box for piece_list and board_list)
        self.cypher_list = []
        for letter in ["a","b","c","d","e","f","g","h"]:
            for number in range(1,9):
                self.cypher_list.append(letter+str(number))
        
        if self.side == chess.BLACK:
            self.tiles.reverse()
            self.board_list.reverse()
            #self.piece_list.reverse()

    def move(self, move, swap):
        if swap:
            window_swap()
            self.update_piece_list(self.cboard.parse_san(move).uci())
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

    def update_piece_list(self,uci_str):
        start_square = uci_str[0:2]
        end_square = uci_str[2:4]
        start_index = self.cypher_list.index(start_square) 
        end_index = self.cypher_list.index(end_square)
        # Castling
        if start_square == "e1" and (end_square == "c1" or end_square == "g1") and self.piece_list[start_index] == 11: # white castle
            if end_square == "c1": # king side
                self.piece_list[32] = None
                self.piece_list[40] = 7 # white rook to f1
                self.piece_list[56] = None
                self.piece_list[48] = 11 # white king to g1 
            else: # queen side
                self.piece_list[0] = None
                self.piece_list[24] = 7 # white rook to d1
                self.piece_list[32] = None
                self.piece_list[16] = 11 # white king to c1

        elif start_square == "e8" and (end_square == "g8" or end_square == "c8") and self.piece_list[start_index] == 5: # black castle
            if end_square == "e8": # king side
                self.piece_list[39] = None
                self.piece_list[47] = 1 # black rook to f8 
                self.piece_list[55] = 5 # black king to g8
                self.piece_list[63] = None
            else: # queen side
                self.piece_list[39] = None
                self.piece_list[31] = 1 # black rook to d8
                self.piece_list[23] = 5 # black king toc8
                self.piece_list[7] = None
        # Promotion
        elif len(uci_str) > 4:
            "NOTE: Currently my implementation assumes promotion to queen"
            # If promotion to other pieces becomes implemented, might have to change piece_list from storing ids to chars
            if self.piece_list[start_index] == 6: # black pawn
                self.piece_list[end_index] = 4
            elif self.piece_list[start_index] == 12: # white pawn
                self.piece_list[end_index] = 10
            else:
                print("PROMOTION ERROR, THIS SHOULD NOT BE SEEN")
            self.piece_list[start_index] = None
            
        # Normal case
        else:
            self.piece_list[end_index] = self.piece_list[start_index]
            self.piece_list[start_index] = None

"Takes in two indices and a board class, returns corresponding UCI string"
def indices_to_move(i1, i2, board):
    if i1 == None or i2 == None:
        return None
    "White promotion to Queen"
    if board.piece_list[i1] == 12 and i1 in range(6,63,8):
        return board.cypher_list[i1] + board.cypher_list[i2] + "q"
    "Black promotion to Queen"
    if board.piece_list[i1] == 6 and i1 in range(1,58,8):
        return board.cypher_list[i1] + board.cypher_list[i2] + "q"
    return board.cypher_list[i1] + board.cypher_list[i2]

