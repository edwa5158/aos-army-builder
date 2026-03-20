from __future__ import annotations

import json
from enum import Enum

from attr import dataclass

from army.constants import Keywords, Timing
from dice.dice import Dice


class Effect:
    def __init__(
        self, desc: str, timing: Timing | None = None, dice: Dice | None = None
    ):
        self.desc: str = desc
        self.dice: Dice | None = dice
        self.timing: Timing | None = timing

    def to_json(self) -> str:
        result: dict = {
            "desc": self.desc,
            "dice": self.dice.to_json() if self.dice else None,
            "timing": self.timing.to_json() if self.timing else None,
        }

        return json.dumps(result)

    @staticmethod
    def from_json(effect_json: str) -> Effect:
        input: dict = json.loads(effect_json)
        d: str | None = input.get("dice", None)
        t: str | None = input.get("timing", None)
        e = Effect(input.get("desc", ""))
        if d:
            e.dice = Dice.from_json(d)
        if t:
            e.timing = Timing.from_json(t)
        return e


class Ability:
    def __init__(self, name: str):
        self.name: str = name
        self.desc: str
        self.effect: Effect
        self.timing: Timing
        self.keywords: list[Keywords]


@dataclass
class Tag:
    tag: str


class WeaponType(Enum):
    MELEE = "melee"
    RANGED = "ranged"


@dataclass
class WeaponProfile:
    name: str
    tags: list[Tag]
    attack: int
    hit: int
    wound: int
    rend: int
    damage: int
    weapon_type: WeaponType
    range: int


class BattleProfile:
    def __init__(
        self, unit_size: int, points: int, can_be_reinforced: bool, base_size: str = ""
    ):
        self.unit_size: int = unit_size
        self.points: int = points
        self.can_be_reinforced: bool = can_be_reinforced
        self.base_size: str = base_size


class Unit:
    def __init__(self, name):
        self.name: str = name
        self.num_models: int
        self.move: int
        self.save: int
        self.control: int
        self.health: int
        self.weapon_profiles: list[WeaponProfile]
        self.url: str
        self.abilities: list[Ability] = []
        self.keywords: list[Keywords] = []
        self.battle_profile: BattleProfile
        self._is_reinforced: bool = False
        self._points: int = 0

    @property
    def is_hero(self) -> bool:
        return Keywords.HERO in self.keywords

    @property
    def is_reinforced(self) -> bool:
        return self._is_reinforced

    @is_reinforced.setter
    def is_reinforced(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError()
        if not value:
            self._is_reinforced = value
        elif self.battle_profile.can_be_reinforced:
            self._is_reinforced = value
        else:
            raise ValueError(f"cannot reinforce {self.name}; it's not reinforceable")

    @property
    def points(self) -> int:
        if self._is_reinforced:
            self._points = self.battle_profile.points * 2
        else:
            self._points = self.battle_profile.points
        return self._points


class Regiment:
    def __init__(self):
        self.units: list[Unit] = []
        self.is_valid: bool = False
        self.is_general_unit: bool = False
        self.has_hero: bool = False
        self.points_total: int = 0

    def add_unit(self, unit: Unit) -> None:
        self.units.append(unit)
        self.has_hero = self.has_hero or unit.is_hero
        self.points_total += unit.points

    @property
    def max_units(self) -> int:
        return 4 if self.is_general_unit else 3

    def validate(self) -> bool:
        r: bool = True
        r &= self.has_hero
        return r


class ArmyRoster:
    def __init__(self):
        self.name: str
        self.regiments: list[Regiment]

    def add_regiment(self, regiment: Regiment) -> None:
        self.regiments.append(regiment)
