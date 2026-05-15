import json
import threading
from types import TracebackType
from typing import Dict, Any

DATA_FILE = "data.json"

class DataManager:
    def __init__(self, data_file: str):
        self._data_file: str = data_file
        self.lock = threading.Lock()
        self._data: Dict[str, Any] = {}
    
    def __enter__(self) -> Dict[str, Any]:
        self.lock.__enter__()
        try:
            with open(self._data_file) as data_file:
                self._data = json.load(data_file)
        except:
            print(f"Failed to load {self._data_file}")
            self._data = {}
        return self._data

    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, trace: TracebackType) -> None:
        with open(self._data_file, "w") as data_file:
            json.dump(self._data, data_file)
        self.lock.__exit__(type, value, trace)

DATA = DataManager(DATA_FILE)