from data import DATA

KEY = "init"

def reset():
    with DATA.lock:
        DATA.get()[KEY] = {}
        DATA.write()

def add(name: str, value: int):
    with DATA.lock:
        DATA.get()[KEY][name] = value
        DATA.write()

def get_formatted():
    with DATA.lock:
        init = DATA.get()[KEY]
    header = "**Initiative**\n"
    roll_list = [(init[name], name) for name in init]
    roll_list.sort(reverse=True)
    contents = "\n".join(f"{roll}: {name}" for roll, name in roll_list)
    return header + contents