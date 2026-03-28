from army.data_model import ArmyRoster
from army.constants import Keyword, Keywords, Timing
from army.data_model import (
    Ability,
    BattleProfile,
    Effect,
    Regiment,
    Warscroll,
    WeaponProfile,
    WeaponType,
)
from dice.dice import Dice

d = Dice(4, 6)
t = Timing.YOUR_COMBAT_PHASE
e = Effect("a description effect", t, d)
e_no_dice = Effect("a description effect", t, None)


def clanrats() -> Warscroll:
    ws = Warscroll(
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
    return ws


def test_effect_json():

    e_json = e.to_json()
    e2 = Effect.from_json(e_json)

    assert e == e2


def test_effect_no_dice_json():

    e_json = e_no_dice.to_json()
    e2 = Effect.from_json(e_json)

    assert e_no_dice == e2


def test_ability_json():
    a = Ability(
        "an ability", "a description", e, t, Keywords([Keyword.CHAMPION, Keyword.CHAOS])
    )
    a_json = a.to_json()
    a2 = Ability.from_json(a_json)
    assert a == a2


def test_weapon_type_json():
    melee = WeaponType.MELEE
    melee_json = melee.to_json()
    melee2 = WeaponType.from_json(melee_json)
    assert melee == melee2


def test_weapon_profile_json():
    wp = WeaponProfile(
        "Rusty Weapon", ["Crit (Auto-wound)"], 2, 4, 5, 0, 1, WeaponType.MELEE, "MELEE"
    )
    wp2 = WeaponProfile.from_json(wp.to_json())
    assert wp == wp2


def test_battle_profile_json():
    bf = BattleProfile(20, 150, True, "25mm")
    bf2 = BattleProfile.from_json(bf.to_json())
    assert bf == bf2


def test_unit_json():
    ws = clanrats()
    ws2 = Warscroll.from_json(ws.to_json())
    assert ws == ws2


def test_unit_points():
    ws = clanrats()
    ws.is_reinforced = False
    assert ws.points == ws.battle_profile.points

    ws.is_reinforced = True
    assert ws.points == ws.battle_profile.points * 2

    ws.is_reinforced = False
    ws.battle_profile.can_be_reinforced = False

    try:
        ws.is_reinforced = True
    except ValueError:
        assert ws.points == ws.battle_profile.points


def test_unit_hero():
    u = clanrats()
    assert not u.is_hero


def test_unit_reinforced():
    u = clanrats()
    u.is_reinforced = False
    assert not u.is_reinforced

    u.is_reinforced = True
    assert u.is_reinforced

    try:
        u.is_reinforced = 1  # type: ignore
    except ValueError:
        return


def test_regiment_equals():
    r = Regiment()
    r.add_unit(clanrats())
    r2 = r
    assert r == r2


def test_regiment_general():
    r = Regiment()
    r.add_unit(clanrats())
    r.is_general_regiment = True

    assert r.is_general_regiment

    assert r.max_units == 4

    r.is_general_regiment = False
    assert r.max_units == 3


def test_regiment_valid():
    r = Regiment()
    r.add_unit(clanrats())

    assert not r.is_valid
    u = clanrats()
    u.keywords.add(Keyword.HERO)
    r.add_unit(u)

    assert r.is_valid

def test_army_roster():
    ar = ArmyRoster()
    ar.name = "The Regiment"

    r1 = Regiment()
    r1.add_unit(clanrats())

    ar.add_regiment(r1)

    assert len(ar.regiments) == 1