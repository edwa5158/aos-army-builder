import json
from pathlib import Path
from typing import Protocol, Self


class JsonSerializable(Protocol):
    def to_json(self) -> dict: ...

    @classmethod
    def from_json(cls, data: dict) -> Self: ...


def save_config(obj: JsonSerializable, file_path: Path) -> None:
    with open(file_path, "a") as f:
        payload: dict = obj.to_json()
        item: dict = {"type": str(type(obj)), "version": 0, "payload": payload}
        json.dump(item, f, indent=4)


# TODO: create a load_serialization function
