import data

KEY = "init"

def reset():
    data.get()[KEY] = {}
    data.write()

def add(name: str, value: int):
    data.get()[KEY][name] = value
    data.write()

def get_formatted():
    init = data.get()[KEY]
    header = "**Initiative**\n"
    roll_list = [(init[name], name) for name in init]
    roll_list.sort(reverse=True)
    contents = "\n".join(f"{roll}: {name}" for roll, name in roll_list)
    return header + contents