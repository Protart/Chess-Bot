import pyautogui 
import time
import cv2
from PIL import Image 
import os 
from mse import mse
import numpy as np

time.sleep(5)

pieces = [Image.open(f'pieces/{i}') for i in os.listdir(r'H:\yt\Chess\pieces')]
piece_name = [i[:-4] for i in os.listdir(r'H:\yt\Chess\pieces')]

Board_with_square_names = []

for o in range(8, 0, -1):
    L = []
    for i in 'abcdefgh':
        L.append(i + str(o))
    Board_with_square_names.append(L)


def get_position():
    ss = pyautogui.screenshot(region=(289, 169, 800, 800))

    ss.save('k.png')

    L = ['*' for i in range(8)]
    Board = [L.copy() for o in range(8)]

    for C in range(8):
        for R in range(8):
            square = ss.crop((C*100, R*100, (C+1)*100, (R+1)*100))
            # name = str(C) + str(R) + '.png'
            # square.save(name)
            for i in pieces:
                if mse(np.array(square), np.array(i)) < 1000:
                    Board[R][C] = piece_name[pieces.index(i)]
    return Board
    # for R in range(8):
    #     for C in range(8):
    #         if Board[R][C] == 'd' or Board[R][C] == 'w':
    #             Board[R][C] = ''

    #         elif Board[R][C]




