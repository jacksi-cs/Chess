"Controls input on terminal and gathering necessary information to decide the next move."

import chess, pyautogui
from board import Board
from eval import first_move, random_move

# After mouse macro will alt-tab back into terminal for next input
def terminal_swap():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

if __name__ == "__main__":
    input("Press enter to start game...")
    
    while True:
        side = input("What side are you?")

        if side.lower() == "white":
            board = Board(chess.WHITE)
            break
        elif side.lower() == "black":
            board = Board(chess.BLACK)
            break
        else:
            print("Not a valid side. Type 'white' or 'black'.")

    if board.side == chess.WHITE:
        while not board.cboard.is_checkmate():
            print(board.cboard)
            board.move(random_move(board.cboard))
            print(board.cboard)
            terminal_swap()
            opp_move = input("Input AN of black's move: ")
            board.move(opp_move)
    
    elif board.side == chess.BLACK:
        while not board.cboard.is_checkmate():
            print(board.cboard)
            opp_move = input("Input AN of white's move: ")
            board.move(opp_move)
            print(board.cboard)
            board.move(random_move(board.cboard))
            terminal_swap()