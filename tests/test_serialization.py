import os
import os.path
from pathlib import Path

from army.constants import Keyword, Keywords, Timing
from army.data_model import Effect
from army.serialization import save_config
from dice.dice import Dice


def test_save_config_keywords() -> None:
    p = Path("./.cache/serialization_files")
    p.mkdir(parents=True, exist_ok=True)
    fp = p.joinpath("keywords.json")
    if fp.exists():
        os.remove(fp)
    obj = Keywords([Keyword.CHAMPION, Keyword.CHAOS])
    save_config(obj, fp)


def test_save_config_effect() -> None:
    p = Path("./.cache/serialization_files")
    p.mkdir(parents=True, exist_ok=True)
    fp = p.joinpath("effect.json")
    if fp.exists():
        os.remove(fp)
    obj = Effect("an effect description")
    save_config(obj, fp)
