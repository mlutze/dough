import re
import random

SUCCESS = "SUCCESS"
ADVANTAGE = "ADVANTAGE"
TRIUMPH = "TRIUMPH"
FAILURE = "FAILURE"
THREAT = "THREAT"
DESPAIR = "DESPAIR"

BLUE = [
    [],
    [],
    [SUCCESS],
    [SUCCESS, ADVANTAGE],
    [ADVANTAGE, ADVANTAGE],
    [ADVANTAGE]
]
BLACK = [
    [],
    [],
    [FAILURE],
    [FAILURE],
    [THREAT],
    [THREAT]
]
GREEN = [
    [],
    [SUCCESS],
    [SUCCESS],
    [SUCCESS, SUCCESS],
    [ADVANTAGE],
    [ADVANTAGE],
    [SUCCESS, ADVANTAGE],
    [ADVANTAGE, ADVANTAGE]
]
PURPLE = [
    [],
    [FAILURE],
    [FAILURE, FAILURE],
    [THREAT],
    [THREAT],
    [THREAT],
    [THREAT, THREAT],
    [FAILURE, THREAT]
]
YELLOW = [
    [],
    [SUCCESS],
    [SUCCESS],
    [SUCCESS, SUCCESS],
    [SUCCESS, SUCCESS],
    [ADVANTAGE],
    [SUCCESS, ADVANTAGE],
    [SUCCESS, ADVANTAGE],
    [SUCCESS, ADVANTAGE],
    [ADVANTAGE, ADVANTAGE],
    [ADVANTAGE, ADVANTAGE],
    [TRIUMPH],
]
RED = [
    [],
    [FAILURE],
    [FAILURE],
    [FAILURE, FAILURE],
    [FAILURE, FAILURE],
    [THREAT],
    [THREAT],
    [FAILURE, THREAT],
    [FAILURE, THREAT],
    [THREAT, THREAT],
    [DESPAIR]
]

DICE = {
    "b": BLUE,
    "k": BLACK,
    "y": YELLOW,
    "g": GREEN,
    "r": RED,
    "p": PURPLE
}

def unfold(roll: str):
    matches = re.findall(r"(\d*)(.)", roll)
    chars = []
    for (num_str, char) in matches:
        if num_str == "":
            num = 1
        else:
            num = int(num_str)
        for _ in range(num):
            chars.append(char)
    return chars

def get_dice(chars):
    dice = []
    for char in chars:
        if char not in DICE:
            raise ValueError(f"Invalid die: {char}")
        dice.append(DICE[char])
    return dice
    
def roll(dice):
    results = []
    for die in dice:
        result = random.choice(die)
        results.append(result)
    return results

def reduce(results):
    successes = results.count(SUCCESS)
    advantages = results.count(ADVANTAGE)
    triumphs = results.count(TRIUMPH)
    failures = results.count(FAILURE)
    threats = results.count(THREAT)
    despairs = results.count(DESPAIR)
    net_success = successes + triumphs - failures - despairs
    net_advantage = advantages - threats
    return (net_success, net_advantage, triumphs, despairs)

def get_report(summary):
    (net_success, net_advantage, triumphs, despairs) = summary
    report = ""
    if net_success >= 0:
        report += f"{net_success} success(es)"
    else:
        report += f"{-net_success} failure(s)"

    if net_advantage > 0:
        report += f", {net_advantage} advantage(s)"
    elif net_advantage < 0:
        report += f", {-net_advantage} threat(s)"

    if triumphs > 0:
        report += f", {triumphs} triumph(s)"

    if despairs > 0:
        report += f", {despairs} despair(s)"
    
    return report

def handle(code: str):
    chars = unfold(code)
    dice = get_dice(chars)
    result = roll(dice)
    summary = reduce(result)
    report = get_report(summary)
    return (report, result)