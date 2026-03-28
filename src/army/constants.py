from __future__ import annotations

from enum import StrEnum
from typing import TypedDict


class KeywordDict(TypedDict):
    """A TypedDict used by Keyword.from_json and Keyword.to_json

    Attributes:
        value (_str_): The value of the Keyword
    """

    keyword: str


class TimingDict(TypedDict):
    """A TypedDict used by Timing.from_json and Timing.to_json

    Attributes:
        value (_str_): The value of the Timing
    """

    timing: str


class Timing(StrEnum):
    PASSIVE = "Passive"

    ANY_HERO_PHASE = "Any Hero Phase"
    ENEMY_HERO_PHASE = "Enemy Hero Phase"
    YOUR_HERO_PHASE = "Your Hero Phase"

    ANY_MOVEMENT_PHASE = "Any Movement Phase"
    ENEMY_MOVEMENT_PHASE = "Enemy Movement Phase"
    YOUR_MOVEMENT_PHASE = "Your Movement Phase"

    ANY_SHOOTING_PHASE = "Any Shooting Phase"
    ENEMY_SHOOTING_PHASE = "Enemy Shooting Phase"
    YOUR_SHOOTING_PHASE = "Your Shooting Phase"

    ANY_CHARGE_PHASE = "Any Charge Phase"
    ENEMY_CHARGE_PHASE = "Enemy Charge Phase"
    YOUR_CHARGE_PHASE = "Your Charge Phase"

    ANY_COMBAT_PHASE = "Any Combat Phase"
    ENEMY_COMBAT_PHASE = "Enemy Combat Phase"
    YOUR_COMBAT_PHASE = "Your Combat Phase"

    END_OF_ANY_TURN = "End of Any Turn"

    def to_json(self) -> TimingDict:
        """returns a dictionary like `{"value": Timing.value}`"""
        return {"timing": self.value}

    @classmethod
    def from_json(cls, data: TimingDict) -> Timing:
        """`data` is a dictionary like `{"value": Timing.value}`"""
        return Timing(data["timing"])


class Keyword(StrEnum):
    CHAMPION = "Champion"
    MUSICIAN = "Musician"
    STANDARD_BEARER = "Standard Bearer"
    INFANTRY = "Infantry"
    HERO = "Hero"
    WARMASTER = "Warmaster"
    UNIQUE = "Unique"
    MONSTER = "Monster"

    RAMPAGE = "Rampage"

    SPELL = "Spell"
    WIZARD = "Wizard"
    WIZARD_2 = "WIZARD (2)"
    WARD_5_PLUS = "Ward (5+)"

    CHAOS = "Chaos"
    SKAVEN = "Skaven"
    VERMINUS = "Verminus"
    MASTERCLAN = "Masterclan"

    def to_json(self) -> KeywordDict:
        """returns a dictionary like `{"value": Keyword.value}`"""
        return {"keyword": self.value}

    @classmethod
    def from_json(cls, data: KeywordDict) -> Keyword:
        """`data` is a dictionary like `{"value": Keyword.value}`"""
        return Keyword(data["keyword"])


class KeywordsDict(TypedDict):
    """A TypedDict used by Keywords.from_json and Keywords.to_json

    Attributes:
        keywords (_list[KeywordDict]_): A list of KeywordDict
    """

    keywords: list[KeywordDict]


class Keywords:
    def __init__(self, keywords: list[Keyword]):
        self.keyword_list: list[Keyword] = keywords

    def __contains__(self, keyword: Keyword):
        return keyword in self.keyword_list

    def __len__(self) -> int:
        return len(self.keyword_list)

    def add(self, keyword: Keyword) -> None:
        if keyword not in self.keyword_list:
            self.keyword_list.append(keyword)

    def to_json(self) -> KeywordsDict:
        """Returns a dictionary `{"keywords": [{"keyword": Keyword.value}, ...}`"""
        result: list[KeywordDict] = [kw.to_json() for kw in self.keyword_list]
        return {"keywords": result}

    @classmethod
    def from_json(cls, data: KeywordsDict) -> Keywords:
        """`data` is a dictionary `{"keywords": [{"keyword": Keyword.value}, ...}`"""

        keywords_input: list[KeywordDict] | None = data.get("keywords", None)
        if not keywords_input:
            return Keywords([])

        keyword_list: list[Keyword] = [Keyword.from_json(kw) for kw in keywords_input]
        return Keywords(keyword_list)

    def __eq__(self, other):
        return self.keyword_list == other.keyword_list
