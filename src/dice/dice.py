from __future__ import annotations

from collections import Counter
from operator import itemgetter
from random import randint
from typing import TypedDict


class RollResult:
    def __init__(self, num_sides: int, num_dice: int):
        self._num_sides: int = num_sides
        self._num_dice: int = num_dice
        self._rolls: list[int] = []
        self._counter: Counter = Counter()

    @property
    def rolls(self) -> list[int]:
        """A list of the raw dice rolles"""
        return self._rolls

    @rolls.setter
    def rolls(self, new_rolls: list[int]) -> None:
        self._rolls = new_rolls
        self._counter = Counter(self._rolls)

    def counts(self) -> dict[int, int]:
        """Returns a the count of each die side rolled, sorted by die side as key"""
        return dict(sorted(self._counter.items(), key=itemgetter(0)))

    def sum(self) -> int:
        """The sume of the individual dice in a roll"""
        return sum(self._rolls)

    def count_n_plus(self, n: int) -> int:
        """Returns the number of dice in the result that exceed `n`"""
        ans: int = 0
        for key, value in self._counter.items():
            if key >= n:
                ans += value
        return ans

    def to_json(self) -> dict:
        result: dict = {
            "num_sides": self._num_sides,
            "num_dice": self._num_dice,
            "results": self._rolls,
        }
        return result

    @classmethod
    def from_json(cls, data: dict) -> RollResult:
        result = RollResult(data.get("num_sides", 0), data.get("num_dice", 0))
        result._rolls = data.get("_results", [])
        return result


class DiceDict(TypedDict):
    num_dice: int
    num_sides: int


class Dice:
    def __init__(self, num_dice: int = 0, num_sides: int = 6):
        self.num_dice: int = num_dice
        self.num_sides: int = num_sides

    def roll_all(self) -> RollResult:
        rolls: list[int] = [self._roll_one() for _ in range(self.num_dice)]
        result = RollResult(self.num_sides, self.num_dice)
        result.rolls = rolls
        return result

    def __repr__(self) -> str:
        return f"{self.num_dice}D{self.num_sides}"

    def __eq__(self, other: Dice) -> bool:  # type:ignore
        return self.num_dice == other.num_dice and self.num_sides == other.num_sides

    def _roll_one(self) -> int:
        return randint(1, self.num_sides)

    def to_json(self) -> DiceDict:
        return {"num_dice": self.num_dice, "num_sides": self.num_sides}

    @classmethod
    def from_json(cls, data: DiceDict) -> Dice:
        return Dice(data.get("num_dice", 0), data.get("num_sides", 0))


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

    def to_json(self) -> dict:
        result: dict = {
            "const": self.const,
            "dice": self.dice.to_json() if self.dice else {},
        }
        return result

    @classmethod
    def from_json(cls, data: dict) -> Amount:
        result = Amount(data.get("const", 0))
        d: DiceDict = data.get("dice", {})
        result.dice = Dice.from_json(d)
        return result
