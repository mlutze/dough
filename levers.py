from __future__ import annotations
from typing import Optional
from data import DATA
import random
import more_itertools

MIN_LEVERS = 3
MIN_GEARS = 3
MAX_GEARS = 7
MAX_GEARS = 10

LEVERS = "levers"
GEARS = "gears"

GREEN = ":green_circle:"
RED = ":red_circle:"


def reset(num_levers: int, num_gears: int) -> str:
    with DATA.lock:
        if not (num_levers >= MIN_LEVERS):
            return f"Minimum of {MIN_LEVERS} levers."
        if not (MIN_GEARS <= num_gears <= MAX_GEARS):
            return f"Minimum of {MIN_GEARS} objects. Maximum of {MAX_GEARS} objects."
        levers = random_solvable_nontrivial_puzzle(num_gears, num_levers)
        levers = [list(lever) for lever in levers]
        DATA.get()[LEVERS] = levers
        DATA.get()[GEARS] = initial_state(num_gears)
        DATA.write()
        return "Puzzle reset."

def pull(lever: int) -> str:
    # change to 0-indexed
    lever -= 1

    with DATA.lock:
        levers = DATA.get()[LEVERS]
        gears = DATA.get()[GEARS]
        levers = [set(lever) for lever in levers]
        if not (0 <= lever < len(levers)):
            return f"There is no lever {lever + 1}." # change to 1-indexed for message

        message = get_full_update_message(gears, levers[lever])
        gears = apply(gears, levers[lever])
        if all(gears):
            message += "\n**A window in the device opens, revealing a delicate gear set!**"
        DATA.get()[GEARS] = gears
        DATA.write()
    return message

def look() -> str:
    with DATA.lock:
        gears = DATA.get()[GEARS]
        num_levers = len(DATA.get[LEVERS])
        message = f"There are {num_levers} levers.\n"
        message += get_full_status_message(gears)
        if all(gears):
            message += "\n**A window in the device opens, revealing a delicate gear set!**"
    return message

def get_update_message(gear: int, state: bool) -> str:
    if gear == 0:
        if state:
            return GREEN + " The **Trade District** emerges from the terrain."
        else:
            return RED + " The **Trade District** descends into the terrain."
    elif gear == 1:
        if state:
            return GREEN + " **The Docks** emerge from the water and terrain."
        else:
            return RED + " **The Docks** descend into the water and terrain."
    elif gear == 2:
        if state:
            return GREEN + " The **South Town** emerges from the terrain."
        else:
            return RED + " The **South Town** descends into the terrain."
    elif gear == 3:
        if state:
            return GREEN + " The **Mead Park** emerges from the terrain."
        else:
            return RED + " The **Mead Park** descends into the terrain."
    elif gear == 4:
        if state:
            return GREEN + " The **Farmland** emerges from the terrain."
        else:
            return RED + " The **Farmland** descends into the terrain."
    elif gear == 5:
        if state:
            return GREEN + " The **Roads** emerge from the terrain."
        else:
            return RED + " The **Roads** descend into the terrain."
    elif gear == 6:
        if state:
            return GREEN + " The **Fleet** emerges from the water."
        else:
            return RED + " The **Fleet** descends into the water."
    else:
        raise Exception("bad lever")


def get_full_update_message(state: list[bool], lever: set[int]) -> str:
    messages = [get_update_message(gear, not(state[gear])) for gear in range(len(state)) if gear in lever]
    return "\n".join(messages)

def get_status_message(gear: int, state: bool) -> str:
    if gear == 0:
        if state:
            return GREEN + " The **Trade District** is visible."
        else:
            return RED + " The **Trade District** is not visible."
    elif gear == 1:
        if state:
            return GREEN + " **The Docks** are visible."
        else:
            return RED + " **The Docks** are not visible."
    elif gear == 2:
        if state:
            return GREEN + " The **South Town** is visible."
        else:
            return RED + " The **South Town** is not visible."
    elif gear == 3:
        if state:
            return GREEN + " The **Mead Park** is visible."
        else:
            return RED + " The **Mead Park** is not visible."
    elif gear == 4:
        if state:
            return GREEN + " The **Farmland** is visible."
        else:
            return RED + " The **Farmland** is not visible."
    elif gear == 5:
        if state:
            return GREEN + " The **Roads** are visible."
        else:
            return RED + " The **Roads** are not visible."
    elif gear == 6:
        if state:
            return GREEN + " The **Fleet** is visible."
        else:
            return RED + " The **Fleet** is not visible."
    else:
        raise Exception("bad lever")

def get_full_status_message(state: list[bool]) -> str:
    messages = [get_status_message(gear, state[gear]) for gear in range(len(state))]
    return "\n".join(messages)

def apply(state: list[bool], lever: set[int]) -> list[bool]:
    new_state = state.copy()
    for gear in lever:
        new_state[gear] = not state[gear]
    return new_state

def random_puzzle(num_gears: int, num_levers: int) -> list[set[int]]:
    return [random_lever(num_gears) for i in range(num_levers)]

def random_lever(num_gears: int) -> set[int]:
    return set(i for i in range(num_gears) if random.choice([False, True]))

def apply_all(state: list[bool], levers: set[set[int]]) -> list[bool]:
    new_state = state.copy()
    for lever in levers:
        new_state = apply(new_state, lever)
    return new_state

def initial_state(num_gears: int) -> list[bool]:
    return [False for _ in range(num_gears)]

def solvable(levers: list[set[int]], num_gears: int) -> bool:
    return solution(levers, num_gears) is not None

def solution(levers: list[set[int]], num_gears: int) -> Optional[set[int]]:
    sols = solutions(levers, num_gears)
    if sols:
        return sols[0]
    else:
        return None

def solutions(levers: list[set[int]], num_gears: int) -> list[tuple]:
    sols = []
    lever_sets = more_itertools.powerset(levers)
    for lever_set in lever_sets:
        if False not in apply_all(initial_state(num_gears), lever_set):
            sols.append(lever_set)
    return sols

def trivially_solvable(levers: list[set[int]], num_gears: int) -> bool:
    trivial_sols = [sol for sol in solutions(levers, num_gears) if trivial(sol)]
    return len(trivial_sols) > 0

def trivial(levers: list[set[int]]) -> bool:
    seen = set()
    for lever in levers:
        for gear in lever:
            if gear in seen:
                return False
            else:
                seen.add(gear)
    return True

def random_solvable_nontrivial_puzzle(num_gears: int, num_levers: int) -> list[set[int]]:
    while True:
        puzzle = random_puzzle(num_gears, num_levers)
        if solvable(puzzle, num_gears) and not trivially_solvable(puzzle, num_gears):
            return puzzle