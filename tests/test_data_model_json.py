from army.constants import Keyword, Keywords, Timing
from army.data_model import (
    Ability,
    BattleProfile,
    Effect,
    Unit,
    WeaponProfile,
    WeaponType,
)
from dice.dice import Dice

d = Dice(4, 6)
t = Timing.YOUR_COMBAT_PHASE
e = Effect("a description effect", t, d)
e_no_dice = Effect("a description effect", t, None)


def clanrats() -> Unit:
    u = Unit(
        "clanrats",
        20,
        6,
        5,
        1,
        1,
        [
            WeaponProfile(
                "Rusty Weapon",
                ["Crit Auto-Wound"],
                2,
                4,
                5,
                0,
                1,
                WeaponType.MELEE,
                "MELEE",
            )
        ],
        "https://wahapedia.ru/aos4/factions/skaven/Clanrats",
        [
            Ability(
                name="Seething Swarm",
                desc="Clanrats overwhelm their enemies with their seemingly endless numbers - biting, stabbing and trampling their own fallen beneath their bloody claws.",
                effect=Effect(
                    desc="You can return D3 slain models to this unit.",
                    timing=Timing.END_OF_ANY_TURN,
                    dice=Dice(1, 3),
                ),
                keywords=Keywords([]),
                timing=Timing.END_OF_ANY_TURN,
            )
        ],
        keywords=Keywords(
            [
                Keyword.INFANTRY,
                Keyword.CHAMPION,
                Keyword.MUSICIAN,
                Keyword.STANDARD_BEARER,
                Keyword.CHAOS,
                Keyword.SKAVEN,
                Keyword.VERMINUS,
            ]
        ),
        battle_profile=BattleProfile(20, 150, True, "25mm"),
    )
    return u


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


def test_BattleProfile_json():
    bf = BattleProfile(20, 150, True, "25mm")

    bf_json = bf.to_json()
    bf2 = BattleProfile.from_json(bf_json)
    assert bf == bf2


def test_Unit_json():
    u = clanrats()
    u_json = u.to_json()

    u2 = Unit.from_json(u_json)

    assert u == u2


def test_Unit_points():
    u = clanrats()
    u.is_reinforced = False
    assert u.points == u.battle_profile.points

    u.is_reinforced = True
    assert u.points == u.battle_profile.points * 2

    u.is_reinforced = False
    u.battle_profile.can_be_reinforced = False

    try:
        u.is_reinforced = True
    except ValueError:
        assert u.points == u.battle_profile.points


def test_Unit_hero():
    u = clanrats()
    assert not u.is_hero


def test_Unit_reinforced():
    u = clanrats()
    u.is_reinforced = False
    assert not u.is_reinforced

    u.is_reinforced = True
    assert u.is_reinforced

    try:
        u.is_reinforced = 1  # type: ignore
    except ValueError:
        assert True
