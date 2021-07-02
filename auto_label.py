from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pyautogui
from os import listdir
from os.path import isfile, join
from board import window_swap
from operator import sub, add
import random
from natsort import os_sorted
import sys


def capture_board():
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)


    # Generating all possible combinations of pieces on the board
    poss_comb = [(Q,R,B,N,P,q,r,b,n,p,Q+R+B+N+P+q+r+b+n+p+2) for Q in range(0,3) for R in range(0,3) for B in range(0,3) for N in range(0,4) for P in range(0,9) for q in range(0,3) for r in range(0,3) for b in range(0,3) for n in range(0,4) for p in range(0,9)]

    # Randomly generating FEN strings using Bernd's Random FEN Generator 
    fen_list = []
    for i in range(0,5):
        comb = poss_comb[random.randrange(0,len(poss_comb))]
        end_url = ','.join([str(j) for j in comb])
        driver.get("http://bernd.bplaced.net/fengenerator/fengenerator.html?"+end_url)
        for k in range(0,1):
            generate_fen = driver.find_element_by_tag_name("input")
            generate_fen.click()
            fen_string = driver.find_element_by_name("fen")
            fen_string = driver.execute_script("return arguments[0].value;", fen_string)
            fen_list.append(fen_string)

    # Input all generated FEN strings into chess.com and save the resulting board (and its flipped version)

    driver.get("https://www.chess.com/analysis")

    for fen_str in fen_list:
        new_analysis = driver.find_element_by_xpath("(//button[@class='secondary-controls-button'])[2]")
        new_analysis.click()
        load_fen = driver.find_element_by_xpath("(//button[@class='accordion-trigger'])[2]")
        load_fen.click()
        paste_fen = driver.find_element_by_xpath("(//input[@class='ui_v5-input-component'])")
        paste_fen.click()
        pyautogui.write(fen_str)
        load = driver.find_element_by_xpath("//button[@class='ui_v5-button-component ui_v5-button-primary ui_v5-button-small load-from-fen-button']")
        load.click()

        modified_fen = fen_str.split(" ", 1)[0]
        modified_fen = modified_fen.replace("/", "")

        img = driver.find_element_by_xpath("//chess-board")
        img.screenshot('demo_images/' + modified_fen + '_nf.png')
        flip = driver.find_element_by_xpath("(//button[@class='secondary-controls-button'])[1]")
        flip.click()
        img = driver.find_element_by_xpath("//chess-board")
        img.screenshot('demo_images/' + modified_fen + '_f.png')
        flip.click()
    driver.close()

"Before call to auto_label(), make sure that labelImg is set up and alt + tab ready"
# NOTE: Make sure that the labelImg window is maximized
def auto_label():
    piece_size = {
        "R" : (92,108),
        "K" : (111,120),
        "P" : (83,101),
        "B" : (93,114),
        "Q" : (110,110),
        "N" : (108,114)
    }

    move_size = {
        "R" : (40,46),
        "K" : (49,55),
        "P" : (39,38),
        "B" : (42,52),
        "Q" : (50,49),
        "N" : (49,51)
    }

    nf_coord_list = [(433+126*x,105+126*y) for y in range(0,8) for x in range(0,8)] # Starting from top left (a8 if white as FEN string starts there)
    f_coord_list = nf_coord_list[::-1]

    file_names = [f for f in os_sorted(listdir("demo_images")) if isfile(join("demo_images", f))]

    if (len(file_names) == 0):
        print("ERROR: No files in directory!")
    else:
        window_swap()
        time.sleep(1)
        
        for file_name in file_names:
            board_info = file_name.split("_", 1) # board_info[0] is fen string, ...[1] is flipped or not flipped
            if board_info[1] == "f.png":
                coord_list = f_coord_list
            else:
                coord_list = nf_coord_list    
            
            counter = 0
            for i in range(0,len(board_info[0])):
                file_char = file_name[i]
                if file_char.isdigit():
                    counter += int(file_char)
                else:
                    piece = piece_size.get(file_char.capitalize()) # Tuple with the dimensions of the piece
                    half_piece = move_size.get(file_char.capitalize())
                    start_point = tuple(map(sub, coord_list[counter], half_piece)) # Top left of the bounding box
                    end_point = tuple(map(add, start_point, piece)) # Bottom right of the bounding box
                    counter += 1

                    pyautogui.press('w')
                    pyautogui.moveTo(start_point[0], start_point[1])
                    pyautogui.dragTo(end_point[0], end_point[1], button='left')
                    pyautogui.write(file_char)
                    pyautogui.press('enter', presses=2, interval=0.01)
                
            pyautogui.keyDown('ctrl')
            pyautogui.press('s')
            pyautogui.keyUp('ctrl')
            pyautogui.press('d')


if __name__ == "__main__":
    if (len(sys.argv) == 1):
        capture_board()
        auto_label()
    else:
        for arg in sys.argv:
            if arg in ("-c", "--capture"):
                capture_board()
            elif arg in ("-l", "--label"):
                auto_label()