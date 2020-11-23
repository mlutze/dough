

INIT = {}

def reset():
    global INIT
    INIT = {}

def add(name: str, value: int):
    global INIT
    INIT[name] = value

def get_formatted():
    header = "Initiative\n"
    roll_list = [(INIT[name], name) for name in INIT]
    roll_list.sort(reverse=True)
    contents = "\n".join(f"{roll}: {name}" for roll, name in roll_list)
    return header + contents