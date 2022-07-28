from __future__ import annotations
from typing import Optional
import random
import more_itertools

NUM_LEVERS = 7
NUM_GEARS = 7

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

# for gears in range(1, 11):
#     for levers in range(1, 11):
#         ok = 0
#         triv = 0
#         for _ in range(100):
#             puzzle = random_puzzle(gears, levers)
#             if (solvable(puzzle, gears)):
#                 ok += 1
#             if trivially_solvable(puzzle, gears):
#                 triv += 1
#         print(gears, levers, ok, triv)

levers = random_solvable_nontrivial_puzzle(NUM_GEARS, NUM_LEVERS)
state = [False for _ in range(NUM_GEARS)]

while False in state:
    # print(f"Solvable: {solvable(NUM_GEARS, levers)}")
    print(state)
    input_ = input("Pull a lever: ")
    if input_ == "?":
        print("Solution: ", solution(levers, NUM_GEARS))
    else:
        lever_num = int(input_)
        if lever_num == 0:
            levers = random_solvable_nontrivial_puzzle(NUM_GEARS, NUM_LEVERS)
            state = [False for _ in range(NUM_GEARS)]
        else:
            lever = levers[lever_num - 1]
            state = apply(state, lever)

print("Success!")