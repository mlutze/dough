from more_itertools import chunked
from typing import List, Tuple

from data import DATA

KEY = "quests"
UNCHECKED = 0
CHECKED = 1
FAILED = 2

UNCHECKED_SYM = ":white_square_button:"
CHECKED_SYM = ":white_check_mark:"
FAILED_SYM = ":x:"

def get() -> List[Tuple[int, str]]:
    with DATA as data:
        return data[KEY]

def add(quest: str) -> None:
    with DATA as data:
        data[KEY].append((UNCHECKED, quest))

def remove(quest_num: int) -> None:
    with DATA as data:
        index = quest_num - 1
        del data[KEY][index]

def check(quest_num: int) -> None:
    with DATA as data:
        index = quest_num - 1
        _, quest = data[KEY][index]
        data[KEY][index] = (CHECKED, quest)

def fail(quest_num: int) -> None:
    with DATA as data:
        index = quest_num - 1
        _, quest = data[KEY][index]
        data[KEY][index] = (FAILED, quest)

def uncheck(quest_num: int) -> None:
    with DATA as data:
        index = quest_num - 1
        _, quest = data[KEY][index]
        data[KEY][index] = (UNCHECKED, quest)

def format_quest(num: int, quest: Tuple[int, str]) -> str:
    syms = {
        CHECKED: CHECKED_SYM,
        UNCHECKED: UNCHECKED_SYM,
        FAILED: FAILED_SYM,
    }
    status, name = quest
    return f"{syms[status]} {num}. {name}"

def get_formatted() -> List[str]:
   d = get()
   header = "**Quests**"
   groups = chunked((format_quest(i, quest) for i, quest in enumerate(d, 1)), 5)
   contents =  ["\n".join(quests) for quests in groups]
   return [header] + contents
