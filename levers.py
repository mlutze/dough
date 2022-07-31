from __future__ import annotations
from typing import Optional
from data import DATA
import random
import more_itertools

NUM_LEVERS = 6
NUM_GEARS = 6

LEVERS = "levers"
GEARS = "gears"


def init() -> None:
    with DATA.lock:
        levers = random_solvable_nontrivial_puzzle(NUM_GEARS, NUM_LEVERS)
        levers = [list(lever) for lever in levers]
        DATA.get()[LEVERS] = levers
        DATA.get()[GEARS] = initial_state(NUM_GEARS)
        DATA.write()

def pull(lever: int) -> str:
    if not (1 <= lever <= NUM_LEVERS):
        return f"There is no lever {lever}."
    # change to 0-indexed
    lever -= 1
    with DATA.lock:
        levers = DATA.get()[LEVERS]
        gears = DATA.get()[GEARS]
        levers = [set(lever) for lever in levers]
        message = get_full_message(gears, levers[lever])
        gears = apply(gears, levers[lever])
        if all(gears):
            message += "\n**A window in the device opens, revealing a delicate gear set!**"
        DATA.get()[GEARS] = gears
        DATA.write()
    return message


def get_message(gear: int, state: bool) -> str:
    if gear == 0:
        if state:
            return "The **Trade District** emerges from the terrain."
        else:
            return "The **Trade District** descends into the terrain."
    elif gear == 1:
        if state:
            return "**The Docks** emerge from the water and terrain."
        else:
            return "**The Docks** descend into the water and terrain."
    elif gear == 2:
        if state:
            return "The **South Town** emerges from the terrain."
        else:
            return "The **South Town** descends into the terrain."
    elif gear == 3:
        if state:
            return "The **Mead Park** emerges from the terrain."
        else:
            return "The **Mead Park** descends into the terrain."
    elif gear == 4:
        if state:
            return "The **Farmland** emerges from the terrain."
        else:
            return "The **Farmland** descends into the terrain."
    elif gear == 5:
        if state:
            return "The **Roads** emerge from the terrain."
        else:
            return "The **Roads** descend into the terrain."
    elif gear == 6:
        if state:
            return "The **Fleet** emerges from the water."
        else:
            return "The **Fleet** descends into the water."
    else:
        raise Exception("bad lever")


def get_full_message(state: list[bool], lever: set[int]) -> str:
    messages = [get_message(gear, not(state[gear])) for gear in range(NUM_GEARS) if gear in lever]
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