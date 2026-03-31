from __future__ import annotations

from enum import Enum, StrEnum
from typing import TypedDict

from army.constants import Keyword, Keywords, KeywordsDict, Timing, TimingDict


class EffectDict(TypedDict):
    desc: str


class Effect:
    def __init__(self, desc: str):
        self.desc: str = desc

    def to_json(self) -> EffectDict:
        result: EffectDict = {"desc": self.desc}
        return result

    @classmethod
    def from_json(cls, data: EffectDict, version: int = 0) -> Effect:
        return Effect(
            desc=data["desc"],
        )

    def __eq__(self, other: Effect) -> bool:  # type:ignore
        return self.desc == other.desc


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

    def __eq__(self, other: Ability) -> bool:  # type:ignore
        return (
            self.name == other.name
            and self.desc == other.desc
            and self.effect == other.effect
            and self.timing == other.timing
            and self.keywords == other.keywords
        )


class WeaponAbility(Enum):
    ANTI_X = {
        "name": "Anti-X (+1 Rend)",
        "desc": "Add 1 to this weapon's Rend characteristic if the target "
        + "has the keyword after 'Anti-' or fulfils the condition "
        + "after 'Anti-'. Multiples of this ability are cumulative. "
        + "For example, if a weapon has both Anti-charge (+1 Rend) "
        + "and Anti-HERO (+1 Rend), then add 2 to the Rend characteristic "
        + "of the weapon for attacks that target a HERO that charged "
        + "in the same turn.",
    }
    CHARGE = {
        "name": "Charge (+1 Damage)",
        "desc": "Add 1 to this weapon's Damage characteristic if the "
        + "attacking unit charged this turn.",
    }
    COMPANION = {
        "name": "Companion",
        "desc": "Unless otherwise specified, attacks made by this weapon "
        + "are not affected by friendly abilities that modify hit rolls, "
        + "wound rolls or weapon characteristics, except for those that apply negative modifiers (e.g. 'Covering Fire').",
    }
    CRIT_2_HITS = {
        "name": "Crit (2 Hits)",
        "desc": "If an attack made with this weapon scores a critical hit, "
        + "that attack scores 2 hits on the target unit instead of 1. Make "
        + "a wound roll for each hit.",
    }
    CRIT_AUTO_WOUND = {
        "name": "Crit (Auto-wound)",
        "desc": "If an attack made with this weapon scores a critical hit, "
        + "that attack automatically wounds the target. Make a save roll "
        + "as normal.",
    }
    CRIT_MORTAL = {
        "name": "Crit (Mortal)",
        "desc": "If an attack made with this weapon scores a critical hit, "
        + "that attack inflicts mortal damage on the target unit equal to "
        + "the Damage characteristic of that weapon and the attack "
        + "sequence ends.",
    }
    SHOOT_IN_COMBAT = {
        "name": "Shoot in Combat",
        "desc": "This weapon can be used to make shooting attacks even "
        + "if the attacking unit is in combat.",
    }


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


# TODO: Update "tags" to weapon_abilities; possibly subclass Ability
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

    def __eq__(self, other: WeaponProfile) -> bool:  # type:ignore
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

    def __eq__(self, other: BattleProfile) -> bool:  # type:ignore
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
    def from_json(cls, data: BattleProfileDict) -> BattleProfile:
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


# TODO: Create a new class called "Unit" which represents a specific implementation of the Warscroll in an army
class Warscroll:
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
    def from_json(cls, data: UnitDict) -> Warscroll:
        unit = Warscroll(
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

    def __eq__(self, other: Warscroll) -> bool:  # type:ignore
        return (
            self.name == other.name
            and self.num_models == other.num_models
            and self.move == other.move
            and self.save == other.save
            and self.control == other.control
            and self.health == other.health
            and self.weapon_profiles == other.weapon_profiles
            and self.url == other.url
            and self.abilities == other.abilities
            and self.keywords == other.keywords
            and self.battle_profile == other.battle_profile
            and self._is_reinforced == other._is_reinforced
            and self._points == other._points
        )


class Regiment:
    def __init__(self):
        self.units: list[Warscroll] = []
        self._is_valid: bool = False
        self.is_general_regiment: bool = False
        self.has_hero: bool = False
        self.points_total: int = 0

    def add_unit(self, unit: Warscroll) -> None:
        self.units.append(unit)
        self.has_hero = self.has_hero or unit.is_hero
        self.points_total += unit.points

    @property
    def max_units(self) -> int:
        return 4 if self.is_general_regiment else 3

    @property
    def is_valid(self) -> bool:
        r: bool = True
        r &= self.has_hero
        return r

    def __eq__(self, other: Regiment) -> bool:  # type:ignore
        return (
            self.units == other.units
            and self.is_valid == other.is_valid
            and self.is_general_regiment == other.is_general_regiment
            and self.has_hero == other.has_hero
            and self.points_total == other.points_total
        )


class ArmyRoster:
    def __init__(self):
        self.name: str = ""
        self.regiments: list[Regiment] = []

    def add_regiment(self, regiment: Regiment) -> None:
        self.regiments.append(regiment)
