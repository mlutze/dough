import discord
import time
from data import DATA
LAST_SMACKS = "LAST_SMACKS"
SMACKS_GIVEN = "SMACKS_GIVEN"
SMACKS_RECEIVED = "SMACKS_RECEIVED"


def smack(source: discord.User, target: discord.User):
    with DATA.lock:
        initialize_smacks(source)
        initialize_smacks(target) 
        last_smack = DATA.get()[LAST_SMACKS][str(source.id)]
        if within_day(last_smack):
            return False
        else:
            DATA.get()[SMACKS_GIVEN][str(source.id)] += 1
            DATA.get()[SMACKS_RECEIVED][str(target.id)] += 1
            return  True


# returns true if the given epoch time is within 24 hours of now
def within_day(instant: int) -> bool:
    day_seconds = 24 * 60 * 60
    now = time.time()
    return now - instant < day_seconds

def initialize_smacks(user: discord.User):
    data = DATA.get()
    for key in [LAST_SMACKS, SMACKS_GIVEN, SMACKS_RECEIVED]:
        if key not in data:
            data[key] = {}
        obj = data[key]
        id = str(user.id)
        if id not in obj:
            obj[id] = 0
    DATA.write()

def get_smacks(user: discord.User):
    with DATA.lock:
        initialize_smacks(user)
        given = DATA.get()[SMACKS_GIVEN][user.id]
        received = DATA.get()[SMACKS_RECEIVED][user.id]
        return (given, received)
