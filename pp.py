def is_valid_square(sq):
    if sq[0] not in list('abcdefgh') or sq[1] not in list('12345678'):
        return False
    else:
        return True

print(is_valid_square('f8'))