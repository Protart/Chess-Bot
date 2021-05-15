# from get_stockfish_move import get_move_stockfish
# p1 = [['brw', 'd', 'bbw', 'bqd', 'w', 'd', 'bkw', 'd'], ['bpd', 'bpw', 'bpd', 'bpw', 'd', 'w', 'bpd', 'bpw'], ['w', 'd', 'bnw', 'd', 'w', 'bnd', 'w', 'd'], ['d', 'w', 'd', 'w', 'bpd', 'w', 'd', 'w'], ['w', 'wbd', 'w', 'd', 'wpw', 'd', 'w', 'd'], ['d', 'w', 'd', 'wpw', 'd', 'w', 'd', 'wpw'], ['wpw', 'd', 'wpw', 'd', 'w', 'wpd', 'wpw', 'd'], ['wrd', 'wnw', 'd', 'wqw', 'd', 'wrw', 'wkd', 'w']]
# p2 = [['brw', 'd', 'bbw', 'bqd', 'w', 'd', 'bkw', 'd'], ['bpd', 'bpw', 'bpd', 'bpw', 'd', 'w', 'bpd', 'bpw'], ['w', 'd', 'w', 'd', 'w', 'bnd', 'w', 'd'], ['d', 'w', 'd', 'w', 'bpd', 'w', 'd', 'w'], ['w', 'bnd', 'w', 'd', 'wpw', 'd', 'w', 'd'], ['d', 'w', 'd', 'wpw', 'd', 'w', 'd', 'wpw'], ['wpw', 'd', 'wpw', 'd', 'w', 'wpd', 'wpw', 'd'], ['wrd', 'wnw', 'd', 'wqw', 'd', 'wrw', 'wkd', 'w']]
# print(get_move_stockfish(p1, p2))



# from get_pieces import get_position
# import time

# time.sleep(3)

# print(get_position())


# import time 
# import pyautogui

# time.sleep(3)

# ss = pyautogui.screenshot(region=(371, 169, 800, 800))

# ss.show()

from stockfish import Stockfish


stockfish = Stockfish(r"H:\yt\Chess\stockfish_20090216_x64")

move = stockfish.get_best_move()
stockfish.set_position([move])
stockfish.set_positio
print(stockfish.get_board_visual())