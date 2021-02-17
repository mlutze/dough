import json
import threading
from typing import Dict, Any

DATA_FILE = "data.json"

class UnsafeOperation(Exception):
    pass
class Data:
    def __init__(self, data_file: str):
        self.data_file: str = data_file
        self.data: Dict[str, Any] = None
        self.lock = threading.Lock()
    
    def require_lock(self):
        if not self.lock.locked:
            raise UnsafeOperation

    def read(self):
        self.require_lock()
        try:
            with open(self.data_file) as data_file:
                self.data = json.load(data_file)
        except:
            print(f"Failed to load {self.data_file}")
            self.data = {}

    def write(self):
        self.require_lock()
        with open(self.data_file, "w") as data_file:
            json.dump(self.data, data_file)

    def get(self):
        self.require_lock()
        if self.data is None:
            self.read()
        return self.data

DATA = Data(DATA_FILE)