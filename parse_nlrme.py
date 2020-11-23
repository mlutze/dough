from functools import lru_cache

NLRME = "NLRMEv2.txt"

def parse(filename):
    with open(filename) as infile:
        rolls = {}
        for line in infile:
            line1 = line.strip()
            if line1[:4].isdigit() and len(line1) > 4:
                roll, effect = line1.split(" ", 1)
                rolls[int(roll)] = effect
        return rolls

@lru_cache
def get_rolls():
    global NLRME
    return parse(NLRME)
