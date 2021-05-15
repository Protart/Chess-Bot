import pyautogui 
import time
import cv2
from PIL import Image 
import os 
from mse import mse
import numpy as np
from get_pieces import get_position

Board_with_square_names = []
wra, wr, bra, br = ['a1'], ['h1'], ['a8'], ['h8']


for o in range(8, 0, -1):
    L = []
    for i in 'abcdefgh':
        L.append(i + str(o))
    Board_with_square_names.append(L)


def get_square_coords(sq):
    for R in range(8):
        for C in range(8):
            if Board_with_square_names[R][C] == sq:
                return [R, C]


def is_valid_square(sq):
    if sq[0] not in list('abcdefgh') or sq[1] not in list('12345678'):
        return False
    else:
        return True

def get_move(position1, position2):
    global bra, br, wr, wra
    diff = []
    pieces = []
    for R in range(8):
        for C in range(8):
            if position1[R][C] != position2[R][C]:
                diff.append(Board_with_square_names[R][C])
                pieces.append(position1[R][C])
                pieces.append(position2[R][C])

    empty_squares = len([i for i in pieces if i=='w' or i=='d'])
    pieces= [i[:2] for i in pieces if i != 'w' and i!= 'd']
    p_piece = []
    pp_piece = []
    for i in pieces:
        if pieces.count(i) == 2:
            p_piece.append(i)
            pp_piece.append(i[1])

    else:
        if empty_squares == 2 and 'p' in pp_piece:
            for i in diff:
                if int(i[-1]) == 8 or int(i[-1]) == 1:
                    new_sq = i
            R, C = get_square_coords(new_sq)
            piece_promoted = position2[R][C][1]
            return new_sq+'=' + piece_promoted.upper()


    if 'r' in pp_piece and 'k' in pp_piece:
        piece = p_piece[pp_piece.index('k')]
        for i in diff:
            co = get_square_coords(i)
            if position2[co[0]][co[1]] == piece:
                new_sq = i
                old_sq = [o for o in diff if o != new_sq]

        if 'e1' in old_sq and new_sq == 'g1':
            return 'O-O'

        elif 'e1' in old_sq and new_sq == 'c1':
            return 'O-O-O'

        elif 'e8' in old_sq and new_sq == 'g8':
            return 'O-O'

        elif 'e8' in old_sq and new_sq == 'c8':
            return 'O-O-O'


    else:
        piece = p_piece[0]

    for i in diff:
        co = get_square_coords(i)
        if position2[co[0]][co[1]][:2] == piece:
            new_sq = i
            old_sq = [o for o in diff if o != new_sq][0]



    if piece[1] == 'p':
        out = ''

        if empty_squares == 3:
            out += old_sq[0] + 'x' +new_sq

        elif empty_squares == 2:
            out += new_sq

        else:
            out += old_sq[0] + 'x' + new_sq

        columns = 'abcdefgh'
        attack_squares = []

        if piece[0] == 'w':
            at_n = int(new_sq[1]) + 1

        else:
            at_n = int(new_sq[1]) - 1

        if new_sq[0] != 'a' and new_sq[0] != 'h':
            at_sq1 = columns[columns.index(new_sq[0])+1] + str(at_n)
            at_sq2 = columns[columns.index(new_sq[0])-1] + str(at_n)
            attack_squares.append(at_sq1)
            attack_squares.append(at_sq2)
        
        elif new_sq[0] == 'a':
            at_sq1 = columns[columns.index(new_sq[0])+1] + str(at_n)
            attack_squares.append(at_sq1)

        elif new_sq[0] == 'h':
            at_sq2 = columns[columns.index(new_sq[0])-1] + str(at_n)
            attack_squares.append(at_sq2)
        
        if piece[0] == 'w':

            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'bk':
                    out += '+'

        if piece[0] == 'b':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'wk':
                    out += '+'

        return out

    if piece[1] == 'n':
        out = ''
        if empty_squares == 2:
            out += 'N' + new_sq

        else:
            out += 'N' + 'x' + new_sq

        attack_squares = []
        columns = '00abcdefgh00'
        at_n = [int(new_sq[1]) +2, int(new_sq[1]) -2, int(new_sq[1]) +2, int(new_sq[1]) -2, int(new_sq[1]) +1, int(new_sq[1]) - 1, int(new_sq[1]) +1, int(new_sq[1]) - 1]
        at_l = [columns[columns.index(new_sq[0])+1], columns[columns.index(new_sq[0])+1], columns[columns.index(new_sq[0])-1], columns[columns.index(new_sq[0])-1], columns[columns.index(new_sq[0])-2], columns[columns.index(new_sq[0])-2], columns[columns.index(new_sq[0])+2], columns[columns.index(new_sq[0])+2]]
        attack_squares = [at_l[i] + str(at_n[i]) for i in range(8)]
        attack_squares = [i for i in attack_squares if is_valid_square(i)]
        if piece[0] == 'w':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'bk':
                    out += '+'

        if piece[0] == 'b':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'wk':
                    out += '+'

        return out



    if piece[1] == 'b':
        out = ''
        if empty_squares == 2:
            out+= 'B' + new_sq

        else:
            out+= 'B' + 'x' + new_sq

        attack_squares = []
        columns = 'abcdefgh0000000000'
        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])+1) 
            curr_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])+1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)
        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])+1) 
            curr_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])+1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)
        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])-1) 
            curr_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])-1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)
        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])-1) 
            curr_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])-1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)

        if piece[0] == 'w':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'bk':
                    out += '+'

        if piece[0] == 'b':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'wk':
                    out += '+'

        return out

    if piece[1] == 'q':
        out=''
        if empty_squares == 2:
            out += 'Q' + new_sq

        else:
            out += 'Q' + 'x' + new_sq

        attack_squares = []
        columns = 'abcdefgh0000000000'
        curr_sq = new_sq

        while True:
            at_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])+1) 
            curr_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])+1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)

        curr_sq = new_sq

        while True:
            at_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])+1) 
            curr_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])+1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)

        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])-1) 
            curr_sq = columns[columns.index(curr_sq[0])-1] + str(int(curr_sq[1])-1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)
        
        curr_sq = new_sq
        while True:
            at_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])-1) 
            curr_sq = columns[columns.index(curr_sq[0])+1] + str(int(curr_sq[1])-1)

            if not is_valid_square(at_sq):
                break
            
            R, C = get_square_coords(at_sq)

            if position2[R][C] != 'd' and position2[R][C] != 'w':
                attack_squares.append(at_sq)
                break
            else:
                attack_squares.append(at_sq)

        attack_squares_r = []
        attack_squares_columns = []
        for i in range(1, int(new_sq[1])):
            at_sq = new_sq[0] + str(i)
            attack_squares_r.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C]!= 'd':
                attack_squares_r = [attack_squares_r[-1]]

        for i in range(int(new_sq[1])+1, 9):
            at_sq =new_sq[0] + str(i)
            attack_squares_r.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C]!='d':
                break
        
        for i in range(columns.index(at_sq[0])):
            at_sq = columns[i] + new_sq[1]
            attack_squares_columns.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C] != 'd':
                attack_squares_columns = [attack_squares_columns[-1]]

        for i in range(columns.index(at_sq[0])+1, 9):
            at_sq = columns[i] + new_sq[1]
            attack_squares_columns.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C] != 'd':
                break
        


        for i in attack_squares_r:
            attack_squares.append(i)

        for i in attack_squares_columns:
            attack_squares.append(i)

        if piece[0] == 'w':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'bk':
                    out += '+'

        if piece[0] == 'b':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'wk':
                    out += '+'

        return out 



    if piece[1] == 'r':
        out = ''
        if old_sq == wra[-1] or old_sq == bra[-1]:
            if old_sq == wra[-1]:
                wra.append(new_sq)

            elif old_sq == bra[-1]:
                bra.append(new_sq)

            if empty_squares == 2:
                out += 'Ra' + new_sq

            else:
                out += 'Rax' + new_sq
        
        else:
            if old_sq == wr[-1]:
                wr.append(new_sq)

            elif old_sq == br[-1]:
                br.append(new_sq)

            if empty_squares == 2:
                out += 'R' + new_sq

            else:
                out += 'Rx' + new_sq

        attack_squares = []
        attack_squares_columns = []
        columns = 'abcdefgh'
        for i in range(1, int(new_sq[1])):
            at_sq = new_sq[0] + str(i)
            attack_squares.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C]!= 'd':
                attack_squares = [attack_squares[-1]]

        for i in range(int(new_sq[1])+1, 9):
            at_sq =new_sq[0] + str(i)
            attack_squares.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C]!='d':
                break
        
        for i in range(columns.index(at_sq[0])):
            at_sq = columns[i] + new_sq[1]
            attack_squares_columns.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C] != 'd':
                attack_squares_columns = [attack_squares_columns[-1]]

        for i in range(columns.index(at_sq[0])+1, 9):
            at_sq = columns[i] + new_sq[1]
            attack_squares_columns.append(at_sq)
            R, C = get_square_coords(at_sq)
            if position2[R][C]!= 'w' and position2[R][C] != 'd':
                break

        for i in attack_squares_columns:
            attack_squares.append(i)

        if piece[0] == 'w':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'bk':
                    out += '+'

        if piece[0] == 'b':
            for i in attack_squares:
                R, C = get_square_coords(i)
                if position2[R][C][:2] == 'wk':
                    out += '+'

        return out

    if piece[1] == 'k':

        if empty_squares == 2:
            return 'K' + new_sq

        else:
            return 'Kx' + new_sq


def get_move_stockfish(position2, position1):

    global bra, br, wr, wra
    diff = []
    pieces = []
    for R in range(8):
        for C in range(8):
            if position1[R][C] != position2[R][C]:
                diff.append(Board_with_square_names[R][C])
                pieces.append(position1[R][C])
                pieces.append(position2[R][C])

    empty_squares = len([i for i in pieces if i=='w' or i=='d'])
    pieces= [i[:2] for i in pieces if i != 'w' and i!= 'd']
    p_piece = []
    pp_piece = []
    for i in pieces:
        if pieces.count(i) == 2:
            p_piece.append(i)
            pp_piece.append(i[1])

    else:
        if empty_squares == 2 and 'p' in pp_piece:
            for i in diff:
                if int(i[-1]) == 8 or int(i[-1]) == 1:
                    new_sq = i
                    old_sq = [o for o in diff if o != new_sq][0]
            R, C = get_square_coords(new_sq)
            piece_promoted = position2[R][C][1]
            return old_sq + new_sq


    if 'r' in pp_piece and 'k' in pp_piece:
        piece = p_piece[pp_piece.index('k')]
        for i in diff:
            co = get_square_coords(i)
            if position2[co[0]][co[1]] == piece:
                new_sq = i
                old_sq = [o for o in diff if o != new_sq][0]


        if 'e1' in old_sq and new_sq == 'g1':
            return 'e1g1'

        elif 'e1' in old_sq and new_sq == 'c1':
            return 'e1c1'

        elif 'e8' in old_sq and new_sq == 'g8':
            return 'e8g8'

        elif 'e8' in old_sq and new_sq == 'c8':
            return 'e8c8'


    else:
        piece = p_piece[0]

    for i in diff:
        co = get_square_coords(i)
        if position2[co[0]][co[1]][:2] == piece:
            new_sq = i
            old_sq = [o for o in diff if o != new_sq][0]
            return old_sq + new_sq



    