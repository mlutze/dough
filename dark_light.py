import data

KEY = "dark_light"

def get_dark_light():
    d = data.get()[KEY]
    return d["dark"], d["light"]

def set_dark_light(dark, light):
    data.get()[KEY]["dark"] = dark
    data.get()[KEY]["light"] = light
    data.write()