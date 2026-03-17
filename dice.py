from __future__ import annotations

import json.decoder
from collections import Counter
from operator import itemgetter
from random import randint


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

    def to_json(self) -> str:
        result: dict = {
            "num_sides": self._num_sides,
            "num_dice": self._num_dice,
            "results": self._results,
        }
        return json.dumps(result)

    @staticmethod
    def from_json(result_json: str) -> RollResult:
        input: dict = json.loads(result_json)
        result = RollResult(input.get("num_sides", 0), input.get("num_dice", 0))
        result._results = input.get("_results", [])
        return result


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

    def to_json(self) -> str:
        result: dict = {
            "num_dice": self.num_dice,
            "num_sides": self.num_sides,
            "roll_result": self.roll_result.to_json(),
        }
        return json.dumps(result)

    @staticmethod
    def from_json(dice_json: str) -> Dice:
        input: dict = json.loads(dice_json)
        result = Dice(input.get("num_dice", 0), input.get("num_sides", 0))
        r: str | None = input.get("roll_result", None)
        if r:
            result.roll_result = RollResult.from_json(r)
        return result


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

    def to_json(self) -> str:
        result: dict = {
            "const": self.const,
            "dice": self.dice.to_json() if self.dice else "",
        }
        return json.dumps(result)

    @staticmethod
    def from_json(amount_json: str) -> Amount:
        input: dict = json.loads(amount_json)
        result = Amount(input.get("const", 0))
        d: str | None = input.get("dice", None)
        if d:
            result.dice = Dice.from_json(d)
        return result
