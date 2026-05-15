from data import DATA

KEY = "dark_light"

def get_dark_light():
    with DATA as data:
        d = data[KEY]
        return d["dark"], d["light"]

def set_dark_light(dark: int, light: int):
    with DATA as data:
        data[KEY]["dark"] = dark
        data[KEY]["light"] = light