import json

from typing import Any, Dict

from config import DATABASE_FILE


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)

            cls.filename = DATABASE_FILE
            cls.data = {}

        return cls._instance

    def __init__(self):
        self.load()

    def load(self):
        try:
            if len(self.data.keys()) == 0:
                with open(self.filename, 'r') as file:
                    self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create(self, key: str, value: Any) -> bool:
        if key in self.data:
            return False

        self.data[key] = value
        self.save()

        return True

    def read(self, key: str) -> Any:
        return self.data.get(key)

    def update(self, key: str, value: Dict[str, Any]) -> bool:
        if key not in self.data:
            return False

        self.data[key] = value
        self.save()

        return True
