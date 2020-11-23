from functools import lru_cache

CRITS = "critical-hits-revisited.formatted"

def parse(filename):
    tables = {}
    with open(filename) as infile:
        while table_name := infile.readline().strip():
            table = parse_group(infile)
            tables[table_name] = table
    return tables

def parse_range(string):
    if "-" in string:
        low, high = string.split("-")
        return range(int(low), int(high) + 1)
    else:
        return range(int(string), int(string) + 1)

def parse_group(infile):
    rolls = {}
    lines = []
    while line := infile.readline().strip():
        lines.append(line)
    for line in lines:
        range_, text = line.split(" ", 1)
        for i in parse_range(range_):
            rolls[i] = text
    return rolls

@lru_cache
def get_tables():
    global CRITS
    return parse(CRITS)
