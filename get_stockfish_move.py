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


def get_move_stockfish(position2, position1):
    diff = []
    pieces = []
    for R in range(8):
        for C in range(8):
            if position1[R][C] != position2[R][C]:
                diff.append(Board_with_square_names[R][C])
                pieces.append(position1[R][C])
                pieces.append(position2[R][C])

    if diff == []:
        return False
    
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

                    return new_sq + old_sq


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
            return new_sq +old_sq