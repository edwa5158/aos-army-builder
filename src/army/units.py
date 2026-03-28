from army.data_model import (
    Ability,
    BattleProfile,
    Effect,
    Keyword,
    Warscroll,
    WeaponProfile,
    WeaponType,
)

crit_auto_wound: str = "Crit (Auto-wound)"


clanrats = Warscroll("Clanrats")
clanrats.control = 1
clanrats.health = 1
clanrats.move = 6
clanrats.save = 5
clanrats.weapon_profiles = [
    WeaponProfile(
        "Rusty Weapon", [crit_auto_wound], 2, 4, 5, 0, 1, WeaponType.MELEE, "MELEE"
    )
]
clanrats.url = "https://wahapedia.ru/aos4/factions/skaven/Clanrats"
clanrats.keywords = [
    Keyword.INFANTRY,
    Keyword.CHAMPION,
    Keyword.MUSICIAN,
    Keyword.STANDARD_BEARER,
    Keyword.CHAOS,
    Keyword.SKAVEN,
    Keyword.VERMINUS,
]
clanrats.battle_profile = BattleProfile(20, 150, True, "25mm")
clanrats.is_reinforced = True

seething_swarm = Ability("Seething Swarm")
seething_swarm.effect = Effect("You can return {{D3}} slain models to this unit.")
seething_swarm.desc = "Clanrats overwhelm their enemies with their seemingly endless numbers – biting, stabbing and trampling their own fallen beneath their bloody claws."
# seething_swarm.effect.dice = D3()

clanrats.abilities.append(seething_swarm)


# hasattr(clanrats,"ability")
