from typing import List, Set
import random
import more_itertools

NUM_LEVERS = 10
NUM_GEARS = 10

def apply(state: List[bool], lever: Set[int]) -> List[bool]:
    new_state = state.copy()
    for gear in lever:
        new_state[gear] = not state[gear]
    return new_state

def random_puzzle(num_gears: int, num_levers: int) -> List[Set[int]]:
    return [random_lever(num_gears) for i in range(num_levers)]

def random_lever(num_gears: int) -> Set[int]:
    return set(i for i in range(num_gears) if random.choice([False, True]))

def apply_all(state: List[bool], levers: Set[Set[int]]) -> List[bool]:
    new_state = state.copy()
    for lever in levers:
        new_state = apply(new_state, lever)
    return new_state

def initial_state(num_gears: int) -> List[bool]:
    return [False for _ in range(num_gears)]

def solvable(levers: List[Set[int]], num_gears: int) -> bool:
    lever_sets = more_itertools.powerset(levers)
    for lever_set in lever_sets:
        if False not in apply_all(initial_state(num_gears), lever_set):
            return True
    return False

for gears in range(1, 11):
    for levers in range(1, 11):
        ok = 0
        for _ in range(1000):
            puzzle = random_puzzle(gears, levers)
            if (solvable(puzzle, gears)):
                ok += 1
        print(gears, levers, ok)

# levers = random_puzzle(NUM_GEARS, NUM_LEVERS)
# state = [False for _ in range(NUM_GEARS)]

# while False in state:
#     print(f"Solvable: {solvable(levers)}")
#     print(state)
#     lever_num = int(input("Pull a lever: "))
#     if lever_num == 0:
#         levers = random_puzzle(NUM_GEARS, NUM_LEVERS)
#         state = [False for _ in range(NUM_GEARS)]
#     else:
#         lever = levers[lever_num - 1]
#         state = apply(state, lever)

# print("Success!")