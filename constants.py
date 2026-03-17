from __future__ import annotations

import json
from enum import Enum


class Timing(Enum):
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

    def to_json(self) -> str:
        result: dict[str, str] = {"name": self.name, "value": self.value}
        return json.dumps(result)

    @staticmethod
    def from_json(timing_json: str) -> Timing:
        input: dict = json.loads(timing_json)
        return Timing(input.get("value"))


class Keywords(Enum):
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
