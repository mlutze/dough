from typing import List, Tuple

import data

KEY = "quests"
UNCHECKED = 0
CHECKED = 1
FAILED = 2

UNCHECKED_SYM = ":white_square_button:"
CHECKED_SYM = ":white_check_mark:"
FAILED_SYM = ":x:"

def get() -> List[Tuple[int, str]]:
    return data.get()[KEY]

def add(quest: str) -> None:
    data.get()[KEY].append((UNCHECKED, quest))
    data.write()

def remove(quest_num: int) -> None:
    index = quest_num - 1
    del data.get()[KEY][index]
    data.write()

def check(quest_num: int) -> None:
    index = quest_num - 1
    _, quest = data.get()[KEY][index]
    data.get()[KEY][index] = (CHECKED, quest)
    data.write()

def fail(quest_num: int) -> None:
    index = quest_num - 1
    _, quest = data.get()[KEY][index]
    data.get()[KEY][index] = (FAILED, quest)
    data.write()

def uncheck(quest_num: int) -> None:
    index = quest_num - 1
    _, quest = data.get()[KEY][index]
    data.get()[KEY][index] = (UNCHECKED, quest)
    data.write()

def format_quest(num: int, quest: Tuple[int, str]) -> str:
    syms = {
        CHECKED: CHECKED_SYM,
        UNCHECKED: UNCHECKED_SYM,
        FAILED: FAILED_SYM,
    }
    status, name = quest
    return f"{syms[status]} {num}. {name}"

def get_formatted() -> str:
   d = get()
   header = "**Quests**\n"
   contents =  "\n".join(format_quest(i, quest) for i, quest in enumerate(d, 1))
   return header + contents
