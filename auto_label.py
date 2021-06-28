from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pyautogui
from os import listdir
from os.path import isfile, join
from board import window_swap
from operator import sub, add


def capture_board():
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)


    # Generating all possible combinations of pieces on the board
    # poss_comb = [(Q,R,B,N,P,q,r,b,n,p,Q+R+B+N+P+q+r+b+n+p+2) for Q in range(0,3) for R in range(0,3) for B in range(0,3) for N in range(0,4) for P in range(0,9) for q in range(0,3) for r in range(0,3) for b in range(0,3) for n in range(0,4) for p in range(0,9)]
    poss_comb = [(1,1,1,1,1,1,1,1,1,1,12)]

    # Randomly generating FEN strings using Bernd's Random FEN Generator 
    fen_list = []
    for comb in poss_comb:
        end_url = ','.join([str(i) for i in comb])
        driver.get("http://bernd.bplaced.net/fengenerator/fengenerator.html?"+end_url)
        for i in range(0,10):
            generate_fen = driver.find_element_by_tag_name("input")
            generate_fen.click()
            fen_string = driver.find_element_by_name("fen")
            fen_string = driver.execute_script("return arguments[0].value;", fen_string)
            fen_list.append(fen_string)

    # Input all generated FEN strings into chess.com and save the resulting board (and its flipped version)

    driver.get("https://www.chess.com/analysis")

    print(fen_list)

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
        img.screenshot('auto_images/' + modified_fen + '_nf.png')
        print(type('auto_images/test.png'))
        flip = driver.find_element_by_xpath("(//button[@class='secondary-controls-button'])[1]")
        flip.click()
        img = driver.find_element_by_xpath("//chess-board")
        img.screenshot('auto_images/' + modified_fen + '_f.png')
        flip.click()
    driver.close()

"Before call to auto_label(), make sure that labelImg is set up and alt + tab ready"
# NOTE: Make sure that the labelImg window is maximized
def auto_label():
    piece_size = {
        "R" : (87,111),
        "K" : (109,113),
        "P" : (80,94),
        "B" : (87,115),
        "Q" : (112,113),
        "N" : (99,112)
    }

    nf_coord_list = [(443+126*x,117+126*y) for y in range(0,8) for x in range(0,8)] # Starting from top left (a8 if white as FEN string starts there)
    f_coord_list = nf_coord_list[::-1]

    file_names = [f for f in listdir("auto_images") if isfile(join("auto_images", f))]

    window_swap()
    
    for file_name in file_names:
        print("FILE NAME: ", file_name)
        board_info = file_name.split("_", 1) # board_info[0] is fen string, ...[1] is flipped or not flipped
        if board_info[1] == "f.png":
            coord_list = f_coord_list
        else:
            coord_list = nf_coord_list    
        
        counter = 0
        for i in range(0,len(board_info[0])):
            file_char = file_name[i]
            print("FILE CHAR: ", file_char)
            if file_char.isdigit():
                print("IS DIGIT")
                counter += int(file_char)
            else:
                print("IS NOT DIGIT")
                piece = piece_size.get(file_char.capitalize()) # Tuple with the dimensions of the piece
                half_piece = tuple(0.5*c for c in piece)
                start_point = tuple(map(sub, coord_list[counter], half_piece)) # Top left of the bounding box
                end_point = tuple(map(add, start_point, piece)) # Bottom right of the bounding box
                print(start_point, end_point)
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


# capture_board()
auto_label()