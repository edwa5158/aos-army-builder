from army.constants import Keyword, Keywords, Timing
from army.data_model import Ability, Effect, WeaponProfile, WeaponType
from dice.dice import Dice

d = Dice(4, 6)
t = Timing.YOUR_COMBAT_PHASE
e = Effect("a description effect", t, d)
e_no_dice = Effect("a description effect", t, None)


def test_Effect_json():

    e_json = e.to_json()
    e2 = Effect.from_json(e_json)

    assert e == e2


def test_Effect_no_dice_json():

    e_json = e_no_dice.to_json()
    e2 = Effect.from_json(e_json)

    assert e_no_dice == e2


def test_Ability_json():
    a = Ability(
        "an ability", "a description", e, t, Keywords([Keyword.CHAMPION, Keyword.CHAOS])
    )
    a_json = a.to_json()
    a2 = Ability.from_json(a_json)
    assert a == a2

def test_WeaponType_json():
    melee = WeaponType.MELEE
    melee_json = melee.to_json()
    melee2 = WeaponType.from_json(melee_json)
    assert melee == melee2


def test_WeaponProfile_json():
    crit_auto_wound: str = "Crit (Auto-wound)"
    wp = WeaponProfile(
        "Rusty Weapon", [crit_auto_wound], 2, 4, 5, 0, 1, WeaponType.MELEE, "MELEE"
    )
    wp_json = wp.to_json()
    wp2 = WeaponProfile.from_json(wp_json)
    assert wp == wp2
