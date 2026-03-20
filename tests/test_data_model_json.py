from army.constants import Timing
from army.data_model import Effect
from dice.dice import Dice


def test_Effect_json():
    d = Dice(4, 6)
    t = Timing.YOUR_COMBAT_PHASE
    e = Effect("a description effect", t, d)
    e_json = e.to_json()
    e2 = Effect.from_json(e_json)

    assert e2.desc == e.desc
    assert e2.timing == e.timing
    assert e2.dice == e.dice
    assert e2.dice is not e.dice
