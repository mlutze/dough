import json

DATA_FILE = "data.json"
DATA = None

def read():
    global DATA
    global DATA_FILE
    try:
        with open(DATA_FILE) as data_file:
            DATA = json.load(data_file)
    except:
        print(f"Failed to load {DATA_FILE}")
        DATA = {}

def write():
    global DATA
    global DATA_FILE
    with open(DATA_FILE, "w") as data_file:
        json.dump(DATA, data_file)

def get():
    if DATA is None:
        read()
    return DATA