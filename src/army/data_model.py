from __future__ import annotations

from enum import StrEnum
from typing import NotRequired, TypedDict

from army.constants import Keyword, Keywords, KeywordsDict, Timing, TimingDict
from dice.dice import Dice, DiceDict


class EffectDict(TypedDict):
    """
    Attributes:
        desc (_str_): _Effect description_
        timing (_TimingDict_): _The effect timing_
        dice (_Optional DiceDict_): _Any Dice associated with the effect_
    """

    desc: str
    timing: TimingDict
    dice: NotRequired[DiceDict]


class Effect:
    def __init__(self, desc: str, timing: Timing, dice: Dice | None = None):
        self.desc: str = desc
        self.timing: Timing = timing
        self.dice: Dice | None = dice

    def to_json(self) -> EffectDict:
        result: EffectDict = {"desc": self.desc, "timing": self.timing.to_json()}
        if self.dice:
            result["dice"] = self.dice.to_json()
        return result

    @classmethod
    def from_json(cls, data: EffectDict, version: int = 0) -> Effect:
        return Effect(
            desc=data["desc"],
            timing=Timing.from_json(data["timing"]),
            dice=Dice.from_json(data.get("dice")) if data.get("dice") else None,
        )

    def __eq__(self, other):
        return (
            self.desc == other.desc
            and self.timing == other.timing
            and self.dice == other.dice
        )


class AbilityDict(TypedDict):
    name: str
    desc: str
    effect: EffectDict
    timing: TimingDict
    keywords: KeywordsDict


class Ability:
    def __init__(
        self,
        name: str,
        desc: str,
        effect: Effect,
        timing: Timing,
        keywords: Keywords,
    ):
        self.name: str = name
        self.desc: str = desc
        self.effect: Effect = effect
        self.timing: Timing = timing
        self.keywords: Keywords = keywords

    def to_json(self) -> AbilityDict:
        return {
            "name": self.name,
            "desc": self.desc,
            "effect": self.effect.to_json(),
            "timing": self.timing.to_json(),
            "keywords": self.keywords.to_json(),
        }

    @classmethod
    def from_json(cls, data: AbilityDict) -> Ability:
        return Ability(
            name=data["name"],
            desc=data["desc"],
            effect=Effect.from_json(data["effect"]),
            timing=Timing.from_json(data["timing"]),
            keywords=Keywords.from_json(data["keywords"]),
        )

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.desc == other.desc
            and self.effect == other.effect
            and self.timing == other.timing
            and self.keywords == other.keywords
        )


class WeaponTypeDict(TypedDict):
    weapon_type: "str"


class WeaponType(StrEnum):
    MELEE = "melee"
    RANGED = "ranged"

    def to_json(self) -> WeaponTypeDict:
        return {"weapon_type": self.value}

    @classmethod
    def from_json(cls, data: WeaponTypeDict) -> WeaponType:
        return WeaponType(data["weapon_type"])


class WeaponProfileDict(TypedDict):
    name: str
    tags: list[str]
    attack: int
    hit: int
    wound: int
    rend: int
    damage: int
    weapon_type: WeaponTypeDict
    range: str


class WeaponProfile:
    """
    Attributes:
        name (_str_): _description_
        tags (_list[str]_): _description_
        attack (_int_): _description_
        hit (_int_): _description_
        wound (_int_): _description_
        rend (_int_): _description_
        damage (_int_): _description_
        weapon_type (_WeaponType_): _description_
        range (_str_): _description_
    """

    def __init__(
        self,
        name: str,
        tags: list[str],
        attack: int,
        hit: int,
        wound: int,
        rend: int,
        damage: int,
        weapon_type: WeaponType,
        range: str,
    ):
        self.name: str = name
        self.tags: list[str] = tags
        self.attack: int = attack
        self.hit: int = hit
        self.wound: int = wound
        self.rend: int = rend
        self.damage: int = damage
        self.weapon_type: WeaponType = weapon_type
        self.range: str = range

    def to_json(self) -> WeaponProfileDict:
        result: WeaponProfileDict = {
            "name": self.name,
            "tags": self.tags,
            "attack": self.attack,
            "hit": self.hit,
            "wound": self.wound,
            "rend": self.rend,
            "damage": self.damage,
            "weapon_type": self.weapon_type.to_json(),
            "range": self.range,
        }
        return result

    @classmethod
    def from_json(cls, data: WeaponProfileDict) -> WeaponProfile:
        return WeaponProfile(
            data["name"],
            data["tags"],
            data["attack"],
            data["hit"],
            data["wound"],
            data["rend"],
            data["damage"],
            WeaponType.from_json(data["weapon_type"]),
            data["range"],
        )

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.tags == other.tags
            and self.attack == other.attack
            and self.hit == other.hit
            and self.wound == other.wound
            and self.rend == other.rend
            and self.damage == other.damage
            and self.weapon_type == other.weapon_type
            and self.range == other.range
        )


class BattleProfileDict(TypedDict):
    unit_size: int
    points: int
    can_be_reinforced: bool
    base_size: str


class BattleProfile:
    def __init__(
        self, unit_size: int, points: int, can_be_reinforced: bool, base_size: str = ""
    ):
        self.unit_size: int = unit_size
        self.points: int = points
        self.can_be_reinforced: bool = can_be_reinforced
        self.base_size: str = base_size

    def __eq__(self, other):
        return (
            self.unit_size == other.unit_size
            and self.points == other.points
            and self.can_be_reinforced == other.can_be_reinforced
            and self.base_size == other.base_size
        )

    def to_json(self) -> BattleProfileDict:
        result: BattleProfileDict = {
            "unit_size": self.unit_size,
            "points": self.points,
            "can_be_reinforced": self.can_be_reinforced,
            "base_size": self.base_size,
        }
        return result

    @classmethod
    def from_json(self, data: BattleProfileDict) -> BattleProfile:
        return BattleProfile(
            data["unit_size"],
            data["points"],
            data["can_be_reinforced"],
            data["base_size"],
        )


class UnitDict(TypedDict):
    name: str
    num_models: int
    move: int
    save: int
    control: int
    health: int
    weapon_profiles: list[WeaponProfileDict]
    url: str
    abilities: list[AbilityDict]
    keywords: KeywordsDict
    battle_profile: BattleProfileDict
    _is_reinforced: bool
    _points: int


class Unit:
    def __init__(
        self,
        name: str,
        num_models: int,
        move: int,
        save: int,
        control: int,
        health: int,
        weapon_profiles: list[WeaponProfile],
        url: str,
        abilities: list[Ability],
        keywords: Keywords,
        battle_profile: BattleProfile,
    ):
        self.name: str = name
        self.num_models: int = num_models
        self.move: int = move
        self.save: int = save
        self.control: int = control
        self.health: int = health
        self.weapon_profiles: list[WeaponProfile] = weapon_profiles
        self.url: str = url
        self.abilities: list[Ability] = abilities
        self.keywords: Keywords = keywords
        self.battle_profile: BattleProfile = battle_profile
        self._is_reinforced: bool = False
        self._points: int = 0

    @property
    def is_hero(self) -> bool:
        return Keyword.HERO in self.keywords

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

    def to_json(self) -> UnitDict:
        result: UnitDict = {
            "name": self.name,
            "num_models": self.num_models,
            "move": self.move,
            "save": self.save,
            "control": self.control,
            "health": self.health,
            "weapon_profiles": [wp.to_json() for wp in self.weapon_profiles],
            "url": self.url,
            "abilities": [ability.to_json() for ability in self.abilities],
            "keywords": self.keywords.to_json(),
            "battle_profile": self.battle_profile.to_json(),
            "_is_reinforced": self._is_reinforced,
            "_points": self._points,
        }
        return result

    @classmethod
    def from_json(cls, data: UnitDict) -> Unit:
        unit = Unit(
            data["name"],
            data["num_models"],
            data["move"],
            data["save"],
            data["control"],
            data["health"],
            [WeaponProfile.from_json(wp) for wp in data["weapon_profiles"]],
            data["url"],
            [Ability.from_json(ability) for ability in data["abilities"]],
            Keywords.from_json(data["keywords"]),
            BattleProfile.from_json(data["battle_profile"]),
        )
        unit._is_reinforced = data["_is_reinforced"]
        unit._points = data["_points"]
        return unit


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
