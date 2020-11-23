import random

def d(a, b = None):
    if b is None:
        num = 1
        sides = a
    else:
        num = a
        sides = b
    return sum(random.randrange(1, sides + 1) for i in range(num))