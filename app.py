from stockfish import Stockfish
import time
from get_pieces import get_position
from get_stockfish_move import get_move_stockfish
import pyautogui
import keyboard

stockfish = Stockfish(r"H:\yt\Chess\stockfish_20090216_x64")

Board_with_square_names = []

moves = []

for o in range(8, 0, -1):
    L = []
    for i in 'abcdefgh':
        L.append(i + str(o))
    Board_with_square_names.append(L)

def square_location(sq):
    for R in range(8):
        for C in range(8):
            if Board_with_square_names[R][C] == sq:
                return 289 + C*100 + 50, 169 + R*100 + 50

move = stockfish.get_best_move()
moves.append(move)
x, y = square_location(move[:2])

pyautogui.click(x, y)
time.sleep(0.2)
x, y = square_location(move[2:])
pyautogui.click(x, y)
board = get_position()
for i in board:
    print(i)

while True:
    if keyboard.is_pressed('k'):
        board2 = get_position()
        time.sleep(0.3)
        moves.append(get_move_stockfish(board, board2))
        stockfish.set_position(moves)
        print(stockfish.get_board_visual())
        move = stockfish.get_best_move()
        moves.append(move)
        stockfish.set_position(moves)
        x, y = square_location(move[:2])
        pyautogui.click(x, y)
        time.sleep(0.2)
        x, y = square_location(move[2:])
        pyautogui.click(x, y)
        board = get_position()
        
print(stockfish.get_board_visual())
print(stockfish.get_best_move())



