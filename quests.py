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
    with DATA.lock:
        return DATA.get()[KEY]

def add(quest: str) -> None:
    with DATA.lock:
        DATA.get()[KEY].append((UNCHECKED, quest))
        DATA.write()

def remove(quest_num: int) -> None:
    with DATA.lock:
        index = quest_num - 1
        del DATA.get()[KEY][index]
        DATA.write()

def check(quest_num: int) -> None:
    with DATA.lock:
        index = quest_num - 1
        _, quest = DATA.get()[KEY][index]
        DATA.get()[KEY][index] = (CHECKED, quest)
        DATA.write()

def fail(quest_num: int) -> None:
    with DATA.lock:
        index = quest_num - 1
        _, quest = DATA.get()[KEY][index]
        DATA.get()[KEY][index] = (FAILED, quest)
        DATA.write()

def uncheck(quest_num: int) -> None:
    with DATA.lock:
        index = quest_num - 1
        _, quest = DATA.get()[KEY][index]
        DATA.get()[KEY][index] = (UNCHECKED, quest)
        DATA.write()

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
   print(contents)
   return [header] + contents
