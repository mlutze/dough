from data import DATA

KEY = "dark_light"

def get_dark_light():
    with DATA.lock:
        d = DATA.get()[KEY]
        return d["dark"], d["light"]

def set_dark_light(dark, light):
    with DATA.lock:
        DATA.get()[KEY]["dark"] = dark
        DATA.get()[KEY]["light"] = light
        DATA.write()