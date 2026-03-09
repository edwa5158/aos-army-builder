from collections import Counter
from enum import Enum
from operator import itemgetter
from random import randint

from attr import dataclass


class RollResult:
    def __init__(self, num_sides: int, num_dice: int):
        self._num_sides: int = num_sides
        self._num_dice: int = num_dice
        self._results: list[int] = []
        self._counter: Counter = Counter()

    @property
    def results(self) -> list[int]:
        return self._results

    @results.setter
    def results(self, new_results: list[int]) -> None:
        self._results = new_results
        self._counter = Counter(self._results)

    def counts(self) -> dict[int, int]:
        """Returns a the count of each die side rolled, sorted by die side as key"""
        return dict(sorted(self._counter.items(), key=itemgetter(0)))

    def sum(self) -> int:
        return sum(self._results)

    def count_n_plus(self, n: int) -> int:
        """Returns the number of dice in the result that exceed `n`"""
        ans: int = 0
        for key, value in self._counter.items():
            if key >= n:
                ans += value
        return ans


class Dice:
    def __init__(self, num_dice: int = 0, num_sides: int = 6):
        self.num_dice: int = num_dice
        self.num_sides: int = num_sides
        self.roll_result: RollResult = RollResult(self.num_sides, self.num_dice)

    def roll_all(self) -> RollResult:
        result: list[int] = []
        for i in range(self.num_dice):
            result.append(self._roll_one())
        self.roll_result.results = result
        return self.roll_result

    def _roll_one(self) -> int:
        return randint(1, self.num_sides)


class D3:
    def roll(self) -> int:
        return Dice(1, 3)._roll_one()


class D6:
    def roll(self) -> int:
        return Dice(1, 6)._roll_one()


class Amount:
    def __init__(self, const: int = 0, dice: Dice | None = None):
        self.const: int = const
        self.dice: Dice | None = dice


class Effect:
    def __init__(self, desc: str, dice: Dice | None = None):
        self.desc: str = desc
        self.dice: Dice | None = dice
        self.timing: str


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
    


class Ability:
    def __init__(self, name: str):
        self.name: str = name
        self.desc: str
        self.effect: Effect


@dataclass
class Tag:
    name: str


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
