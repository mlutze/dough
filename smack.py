import discord
import time
from data import DATA
LAST_SMACKS = "LAST_SMACKS"
SMACKS_GIVEN = "SMACKS_GIVEN"
SMACKS_RECEIVED = "SMACKS_RECEIVED"


def try_smack(source: discord.User, target: discord.User):
    with DATA as data:
        initialize_smacks(source, data)
        initialize_smacks(target, data) 
        last_smack = data[LAST_SMACKS][str(source.id)]
        if within_day(last_smack):
            return False
        else:
            data[SMACKS_GIVEN][str(source.id)] += 1
            data[SMACKS_RECEIVED][str(target.id)] += 1
            data[LAST_SMACKS][str(source.id)] = time.time()
            return True


# returns true if the given epoch time is within 24 hours of now
def within_day(instant: int) -> bool:
    day_seconds = 24 * 60 * 60
    now = time.time()
    return now - instant < day_seconds

def initialize_smacks(user: discord.User, data):
    for key in [LAST_SMACKS, SMACKS_GIVEN, SMACKS_RECEIVED]:
        if key not in data:
            data[key] = {}
        obj = data[key]
        id = str(user.id)
        if id not in obj:
            obj[id] = 0

def get_smacks(user: discord.User):
    with DATA as data:
        initialize_smacks(user)
        given = data[SMACKS_GIVEN][str(user.id)]
        received = data[SMACKS_RECEIVED][str(user.id)]
        return (given, received)
