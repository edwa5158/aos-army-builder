import json
from pathlib import Path
from typing import Mapping, Protocol, TypedDict

type JsonObject = Mapping[str, object]


class JsonWritable(Protocol):
    def to_json(self) -> JsonObject: ...


class SerializedItem(TypedDict):
    type: str
    version: int
    payload: JsonObject


def save_config(obj: JsonWritable, file_path: Path) -> None:
    with file_path.open("a", encoding="utf-8") as f:
        payload = obj.to_json()
        item: SerializedItem = {
            "type": type(obj).__qualname__,
            "version": 0,
            "payload": payload,
        }
        json.dump(item, f, indent=4)
