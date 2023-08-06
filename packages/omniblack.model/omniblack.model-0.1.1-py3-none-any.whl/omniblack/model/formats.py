from .abc import Format
from io import TextIOBase
import json


class JSONFormat(Format):
    def load(self, file: TextIOBase) -> dict:
        return json.load(file)

    def loads(self, string: str) -> dict:
        return json.loads(string)

    def dump(self, file: TextIOBase, data: dict) -> None:
        json.dump(data, file, sort_keys=True, indent=4)

    def dumps(self, data) -> str:
        return json.dumps(data, sort_keys=True, indent=4)
