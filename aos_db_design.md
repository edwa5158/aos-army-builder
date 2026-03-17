# SQLite Database Schema for an Age of Sigmar Matched Play Army-List Builder

## Game-driven requirements for list building

Matched play list building (current “Army Composition” framework used with the seasonal rules/battlepacks) is fundamentally a sequence of *roster selections* constrained by points, regiment structure, and “one-of” choices like battle formations and enhancements. The rule structure matters because it determines what must be representable as first-class data (and what can remain as text). citeturn22view1turn19view0turn19view1turn20view1

Army roster creation, at a minimum, needs to support: picking a points limit (commonly 1000 or 2000, but can be any mutually agreed limit), choosing a faction and (optionally) a battle formation, building one or more regiments (including a general’s regiment with extra capacity), optionally adding auxiliary units, optionally adding faction terrain features, choosing enhancements, and choosing up to one each of spell/prayer/manifestation lores. citeturn22view0turn22view1turn19view1

Points are not just for units: if a regiment of renown, faction terrain feature, enhancement, or lore has a points value, it consumes points, and total selections cannot exceed the agreed limit—plus the “half your points in one unit” cap. citeturn22view1turn20view1

Unit legality and costs are “live” and versioned: battle profiles are updated and newer publications supersede older ones. Your schema should therefore support **versioned rules sources** and **roster snapshots** so saved rosters remain historically consistent even after a points update. citeturn22view1turn8view0

## SQLite constraints that shape the schema

SQLite supports foreign keys, but **enforcement is disabled by default unless enabled by the application per connection**, so the schema should be designed assuming you will enable FK enforcement in your app runtime. citeturn17search0turn17search8

SQLite uses dynamic typing and type affinity; your declared column types help correctness at the application layer, but you still want explicit `NOT NULL`, `UNIQUE`, and `CHECK` constraints for data integrity. citeturn17search14turn17search1

`CHECK` constraints are useful for enums and boolean flags, but they **cannot contain subqueries**, which means multi-row roster validation (e.g., “max 5 regiments” or “no more than 1 regiment of renown”) cannot be fully enforced with `CHECK` alone—you’ll enforce those rules in application logic (or triggers, if you choose). citeturn17search2turn20view1turn19view0

If you want flexible “rules predicates” (e.g., regiment option expressions like “0–1 Cursed Soul, Any Infantry”), you can store them as JSON in a `TEXT` column and validate/query via SQLite’s JSON functions when available. citeturn17search3turn17search22

## Reference tables for rules sources and rule-section linking

This layer solves two needs:
- You need **versioning** (because battle profiles and FAQs change). citeturn8view0turn22view1  
- You need **deep links to specific rules sections** (because you want keywords/abilities to reference exact core-rule sections like “3.3 Reinforced Units” or “4.1 Enhancements”). citeturn19view2turn19view3

### Table: `ruleset`
Represents a coherent “rules environment” (e.g., season/battlepack year).

- `ruleset_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL UNIQUE
- `edition_major` INTEGER NOT NULL CHECK (`edition_major` > 0)
- `season_label` TEXT NULL
- `valid_from` TEXT NULL  *(ISO-8601 date)*
- `valid_to` TEXT NULL  *(ISO-8601 date)*
- `notes` TEXT NULL

### Table: `rules_doc`
Represents a *specific published document/revision* (core rules, army composition packet, battle profiles release, battletome, errata, etc.).

- `doc_id` INTEGER PRIMARY KEY
- `ruleset_id` INTEGER NOT NULL REFERENCES `ruleset`(`ruleset_id`) ON DELETE CASCADE
- `doc_type` TEXT NOT NULL CHECK (`doc_type` IN (
  'core_rules','army_composition','battle_profiles','battletome','faction_pack','errata','faq','other'
))
- `title` TEXT NOT NULL
- `short_code` TEXT NOT NULL  *(e.g., `BP_2025_11`, `NH_BP_2025_08`)*  
- `published_on` TEXT NOT NULL  *(ISO-8601 date)*
- `supersedes_doc_id` INTEGER NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE SET NULL
- `canonical_url` TEXT NULL
- `sha256` TEXT NULL CHECK (`sha256` IS NULL OR length(`sha256`) = 64)
- `notes` TEXT NULL
- UNIQUE(`ruleset_id`, `short_code`)

### Table: `rule_section`
Stores “addressable” sections (so abilities can reference exact citations).

- `rule_section_id` INTEGER PRIMARY KEY
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE CASCADE
- `parent_rule_section_id` INTEGER NULL REFERENCES `rule_section`(`rule_section_id`) ON DELETE CASCADE
- `section_code` TEXT NOT NULL  *(e.g., `3.3`, `4.1`, `5.1`)*
- `title` TEXT NOT NULL
- `page_start` INTEGER NULL CHECK (`page_start` IS NULL OR `page_start` >= 0)
- `page_end` INTEGER NULL CHECK (`page_end` IS NULL OR `page_end` >= `page_start`)
- `anchor` TEXT NULL  *(for your own internal deep-linking)*
- `text_body` TEXT NULL  *(optional; you may store excerpts/notes rather than full copyrighted text)*
- `sort_order` REAL NULL
- UNIQUE(`doc_id`, `section_code`)

### Table: `ability_rule_section`
Many-to-many “citations”: an ability can cite multiple sections and vice versa.

- `ability_id` INTEGER NOT NULL REFERENCES `ability`(`ability_id`) ON DELETE CASCADE
- `rule_section_id` INTEGER NOT NULL REFERENCES `rule_section`(`rule_section_id`) ON DELETE CASCADE
- PRIMARY KEY (`ability_id`, `rule_section_id`)

*(Analogous join tables are recommended for units and faction items: `unit_rule_section`, `faction_item_rule_section`.)*

## Unit and faction catalog tables

Your catalog must reflect how the game defines “what a unit is” and how rules are structured:

- A warscroll contains a unit’s characteristics (Move/Health/Control/Save), unit type, keywords, weapons, and abilities. citeturn26view0
- Abilities have a timing, declare instructions, effect, and keywords. citeturn26view0
- Keywords are used as constraints for using abilities and for eligibility/targeting. citeturn26view0turn18view0
- Factions define battle traits, battle formations, enhancements, and lores (and these live in publications, commonly battletomes, plus points in battle profiles). citeturn26view0turn22view1turn12view0

### Table: `grand_alliance`
Battle profiles organize factions under the four grand alliances. citeturn8view0

- `grand_alliance_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL UNIQUE CHECK (`name` IN ('Order','Chaos','Death','Destruction'))
- `notes` TEXT NULL

### Table: `faction`
- `faction_id` INTEGER PRIMARY KEY
- `grand_alliance_id` INTEGER NOT NULL REFERENCES `grand_alliance`(`grand_alliance_id`) ON DELETE RESTRICT
- `name` TEXT NOT NULL UNIQUE
- `slug` TEXT NOT NULL UNIQUE
- `description` TEXT NULL

### Table: `keyword`
Unifies warscroll keywords and ability keywords. citeturn26view0turn18view0

- `keyword_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL UNIQUE  *(store canonical uppercase for stable matching)*
- `kind` TEXT NOT NULL DEFAULT 'both' CHECK (`kind` IN ('unit','ability','both','other'))
- `description` TEXT NULL

### Table: `unit`
A stable identity for a unit across updates/errata (the “generic definition”).

- `unit_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL
- `slug` TEXT NOT NULL UNIQUE
- `is_unique` INTEGER NOT NULL DEFAULT 0 CHECK (`is_unique` IN (0,1))  
  *(UNIQUE units have special roster restrictions—see roster validation; UNIQUE units also can’t be reinforced and can’t receive enhancements.)* citeturn20view0turn19view3
- `notes` TEXT NULL

### Table: `unit_warscroll`
A specific warscroll version (stats/weapons/abilities can change with updates). citeturn22view1turn26view0

- `unit_warscroll_id` INTEGER PRIMARY KEY
- `unit_id` INTEGER NOT NULL REFERENCES `unit`(`unit_id`) ON DELETE CASCADE
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT
- `version_label` TEXT NULL
- `move_inches` REAL NULL CHECK (`move_inches` IS NULL OR `move_inches` >= 0)
- `health` INTEGER NOT NULL CHECK (`health` > 0)
- `control` INTEGER NOT NULL CHECK (`control` >= 0)
- `save_target` INTEGER NULL CHECK (`save_target` IS NULL OR (`save_target` BETWEEN 2 AND 7))  
  *(store “3+” as `3`; allow NULL if a warscroll uses “-” style notation)*
- `unit_type_text` TEXT NULL
- `rules_text` TEXT NULL  *(optional stored text/blob for offline rendering)*
- UNIQUE(`unit_id`, `doc_id`)

### Table: `unit_keyword`
Warscroll keywords bar. citeturn26view0turn18view0

- `unit_warscroll_id` INTEGER NOT NULL REFERENCES `unit_warscroll`(`unit_warscroll_id`) ON DELETE CASCADE
- `keyword_id` INTEGER NOT NULL REFERENCES `keyword`(`keyword_id`) ON DELETE RESTRICT
- PRIMARY KEY (`unit_warscroll_id`, `keyword_id`)

### Table: `weapon_profile`
Warscroll weapons include melee/ranged profiles and characteristics. citeturn26view0turn18view0

Because AoS weapon characteristics can be dice expressions (e.g., `D3`, `2D6`) and symbols, store raw text plus optional numeric helpers.

- `weapon_profile_id` INTEGER PRIMARY KEY
- `unit_warscroll_id` INTEGER NOT NULL REFERENCES `unit_warscroll`(`unit_warscroll_id`) ON DELETE CASCADE
- `name` TEXT NOT NULL
- `weapon_type` TEXT NOT NULL CHECK (`weapon_type` IN ('melee','ranged'))
- `range_text` TEXT NOT NULL  *(e.g., `Melee`, `12"`)*  
- `range_inches` REAL NULL CHECK (`range_inches` IS NULL OR `range_inches` >= 0)
- `attacks_text` TEXT NOT NULL
- `hit_text` TEXT NOT NULL
- `wound_text` TEXT NOT NULL
- `rend_text` TEXT NOT NULL
- `damage_text` TEXT NOT NULL
- `notes` TEXT NULL

### Table: `ability`
A normalized representation of warscroll abilities, faction abilities (battle traits/formations), regiment-of-renown abilities, etc. Abilities have timing, declare instructions, effect, and keywords. citeturn26view0turn18view0

- `ability_id` INTEGER PRIMARY KEY
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT
- `name` TEXT NOT NULL
- `timing_text` TEXT NOT NULL
- `timing_kind` TEXT NOT NULL CHECK (`timing_kind` IN (
  'passive','normal','reaction','deployment','hero_phase','movement_phase','shooting_phase','charge_phase','combat_phase','end_of_turn','other'
))
- `declare_text` TEXT NULL
- `effect_text` TEXT NOT NULL
- `is_passive` INTEGER NOT NULL DEFAULT 0 CHECK (`is_passive` IN (0,1))
- `usage_limit` TEXT NULL  *(e.g., “Once Per Turn (Army)” patterns; keep raw)*
- `icon_kind` TEXT NULL CHECK (`icon_kind` IS NULL OR `icon_kind` IN ('movement','offensive','defensive','shooting','rally','special','control','other'))
- UNIQUE(`doc_id`, `name`)

### Table: `ability_keyword`
- `ability_id` INTEGER NOT NULL REFERENCES `ability`(`ability_id`) ON DELETE CASCADE
- `keyword_id` INTEGER NOT NULL REFERENCES `keyword`(`keyword_id`) ON DELETE RESTRICT
- PRIMARY KEY (`ability_id`, `keyword_id`)

### Table: `unit_ability`
- `unit_warscroll_id` INTEGER NOT NULL REFERENCES `unit_warscroll`(`unit_warscroll_id`) ON DELETE CASCADE
- `ability_id` INTEGER NOT NULL REFERENCES `ability`(`ability_id`) ON DELETE CASCADE
- `display_order` INTEGER NULL CHECK (`display_order` IS NULL OR `display_order` >= 0)
- PRIMARY KEY (`unit_warscroll_id`, `ability_id`)

### Table: `faction_item`
Represents battle traits, battle formations, enhancements, lores, faction terrain, armies of renown—i.e., “faction rule parts” that can be attached to rosters and/or grant abilities. citeturn26view0turn24view2turn12view0

- `faction_item_id` INTEGER PRIMARY KEY
- `faction_id` INTEGER NOT NULL REFERENCES `faction`(`faction_id`) ON DELETE CASCADE
- `kind` TEXT NOT NULL CHECK (`kind` IN ('battle_trait','battle_formation','enhancement','lore','faction_terrain','army_of_renown','other'))
- `subkind` TEXT NULL  
  *(examples: enhancement → `heroic_trait`, `artefact_of_power`; lore → `spell_lore`, `prayer_lore`, `manifestation_lore`)*
- `name` TEXT NOT NULL
- `slug` TEXT NOT NULL
- `is_unique_pick` INTEGER NOT NULL DEFAULT 1 CHECK (`is_unique_pick` IN (0,1))  
  *(most enhancements/artefacts are “only once per army” concepts; rules reinforce uniqueness constraints.)* citeturn24view2turn19view3
- `description` TEXT NULL
- UNIQUE(`faction_id`, `slug`)

### Table: `faction_item_text`
Stores the actual rules text for the item (often sourced from battletomes/faction packs). citeturn22view1turn26view0

- `faction_item_text_id` INTEGER PRIMARY KEY
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE CASCADE
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT
- `rules_text` TEXT NOT NULL
- UNIQUE(`faction_item_id`, `doc_id`)

### Table: `faction_item_points`
Stores points/legality metadata for list building, sourced from battle profiles (where enhancements/formations can have point costs). citeturn12view0turn22view1

- `faction_item_points_id` INTEGER PRIMARY KEY
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE CASCADE
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT  *(battle profiles release)*
- `points` INTEGER NOT NULL DEFAULT 0 CHECK (`points` >= 0)
- `notes` TEXT NULL
- `is_matched_play_legal` INTEGER NOT NULL DEFAULT 1 CHECK (`is_matched_play_legal` IN (0,1))
- UNIQUE(`faction_item_id`, `doc_id`)

## Points and army-construction support tables

### Table: `battle_profile_unit`
This is the list-building “unit entry” (unit size, points, reinforcement legality, base size, notes, regiment options for HEROES, and “relevant keywords” style hints). Battle profiles are explicitly treated as updateable, with newer releases taking precedence. citeturn22view1turn8view0turn12view0

- `battle_profile_unit_id` INTEGER PRIMARY KEY
- `unit_id` INTEGER NOT NULL REFERENCES `unit`(`unit_id`) ON DELETE CASCADE
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT
- `unit_size` INTEGER NOT NULL CHECK (`unit_size` >= 1)
- `points` INTEGER NOT NULL CHECK (`points` >= 0)
- `can_be_reinforced` INTEGER NOT NULL DEFAULT 1 CHECK (`can_be_reinforced` IN (0,1))  
  *(reinforcement rules: doubled model count and doubled points; some units cannot be reinforced; units of size 1 cannot be reinforced; UNIQUE units cannot be reinforced.)* citeturn19view2turn20view0turn12view0
- `base_size_text` TEXT NULL
- `notes` TEXT NULL
- `regiment_options_raw` TEXT NULL  
  *(store the printed regiment options column for HEROES; parse into structured selectors if you want regiment-validation in-db)* citeturn12view0turn20view2
- `moves_to_legends_on` TEXT NULL  *(ISO-8601 date, if present in notes)*
- `is_matched_play_legal` INTEGER NOT NULL DEFAULT 1 CHECK (`is_matched_play_legal` IN (0,1))
- UNIQUE(`unit_id`, `doc_id`)

### Regiment eligibility modeling (recommended)

Because “regiment options” are the rule-driven constraint that tells which units can go into a given HERO’s regiment, and these options are often keyword- or tag-based (e.g., “0–1 Cursed Soul, Any Infantry”), store both:
- the raw printed string (for rendering), and  
- a parsed structure your app can use for validation/UI. citeturn12view0turn20view2turn22view0

#### Table: `regiment_role_tag`
Represents special “can join as …” categorizations that appear in battle profiles notes (e.g., “This Hero can join … as a Cursed Soul”). citeturn12view0turn22view0

- `regiment_role_tag_id` INTEGER PRIMARY KEY
- `faction_id` INTEGER NULL REFERENCES `faction`(`faction_id`) ON DELETE CASCADE
- `name` TEXT NOT NULL
- UNIQUE(`faction_id`, `name`)

#### Table: `unit_regiment_role_tag`
- `unit_id` INTEGER NOT NULL REFERENCES `unit`(`unit_id`) ON DELETE CASCADE
- `regiment_role_tag_id` INTEGER NOT NULL REFERENCES `regiment_role_tag`(`regiment_role_tag_id`) ON DELETE CASCADE
- PRIMARY KEY (`unit_id`, `regiment_role_tag_id`)

#### Table: `regiment_option_selector`
Parsed, structured selectors for a commander’s regiment options (optional but powerful).

- `regiment_option_selector_id` INTEGER PRIMARY KEY
- `battle_profile_unit_id` INTEGER NOT NULL REFERENCES `battle_profile_unit`(`battle_profile_unit_id`) ON DELETE CASCADE  
  *(the commander HERO’s battle profile row)*
- `selector_kind` TEXT NOT NULL CHECK (`selector_kind` IN ('any_unit','unit','keyword','unit_type','regiment_role_tag'))
- `unit_id` INTEGER NULL REFERENCES `unit`(`unit_id`) ON DELETE RESTRICT
- `keyword_id` INTEGER NULL REFERENCES `keyword`(`keyword_id`) ON DELETE RESTRICT
- `unit_type_text` TEXT NULL
- `regiment_role_tag_id` INTEGER NULL REFERENCES `regiment_role_tag`(`regiment_role_tag_id`) ON DELETE RESTRICT
- `min_allowed` INTEGER NOT NULL DEFAULT 0 CHECK (`min_allowed` >= 0)
- `max_allowed` INTEGER NULL CHECK (`max_allowed` IS NULL OR `max_allowed` >= `min_allowed`)
- `notes` TEXT NULL
- CHECK (
  (`selector_kind` = 'unit' AND `unit_id` IS NOT NULL)
  OR (`selector_kind` = 'keyword' AND `keyword_id` IS NOT NULL)
  OR (`selector_kind` = 'unit_type' AND `unit_type_text` IS NOT NULL)
  OR (`selector_kind` = 'regiment_role_tag' AND `regiment_role_tag_id` IS NOT NULL)
  OR (`selector_kind` = 'any_unit')
)

### Table: `regiment_of_renown`
Regiments of Renown are pre-built regiments you can include by spending points, with special restrictions (only one unless notes say otherwise; they can’t use allied faction rules like enhancements/lores; they can’t be your general even if WARMASTER). citeturn20view1turn8view0

- `ror_id` INTEGER PRIMARY KEY
- `name` TEXT NOT NULL UNIQUE
- `doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT
- `points` INTEGER NOT NULL CHECK (`points` >= 0)
- `notes` TEXT NULL

#### Table: `ror_allowed_faction`
- `ror_id` INTEGER NOT NULL REFERENCES `regiment_of_renown`(`ror_id`) ON DELETE CASCADE
- `faction_id` INTEGER NOT NULL REFERENCES `faction`(`faction_id`) ON DELETE CASCADE
- PRIMARY KEY (`ror_id`, `faction_id`)

#### Table: `ror_unit_slot`
Allows repeated unit entries (e.g., two separate “10 Mortek Guard” slots). citeturn8view0turn20view1

- `ror_unit_slot_id` INTEGER PRIMARY KEY
- `ror_id` INTEGER NOT NULL REFERENCES `regiment_of_renown`(`ror_id`) ON DELETE CASCADE
- `slot_index` INTEGER NOT NULL CHECK (`slot_index` >= 0)
- `unit_id` INTEGER NOT NULL REFERENCES `unit`(`unit_id`) ON DELETE RESTRICT
- `unit_size` INTEGER NULL CHECK (`unit_size` IS NULL OR `unit_size` >= 1)
- `is_reinforced` INTEGER NOT NULL DEFAULT 0 CHECK (`is_reinforced` IN (0,1))
- `notes` TEXT NULL
- UNIQUE(`ror_id`, `slot_index`)

## Roster tables for saved army lists

This layer separates:
- “generic” definitions (units/factions/catalog above), from  
- user-specific “instances” (what is actually in a saved roster).  

It also records the roster’s points context and keeps “points snapshots,” because points sources update. citeturn22view1turn8view0

### Table: `app_user`
- `user_id` INTEGER PRIMARY KEY
- `display_name` TEXT NOT NULL
- `email` TEXT NULL UNIQUE
- `created_at` TEXT NOT NULL  *(ISO-8601 timestamp)*
- `last_login_at` TEXT NULL

### Table: `roster`
Army metadata: user ownership, name/description, faction association, points limit, and cached totals.

- `roster_id` INTEGER PRIMARY KEY
- `user_id` INTEGER NOT NULL REFERENCES `app_user`(`user_id`) ON DELETE CASCADE
- `ruleset_id` INTEGER NOT NULL REFERENCES `ruleset`(`ruleset_id`) ON DELETE RESTRICT
- `points_doc_id` INTEGER NOT NULL REFERENCES `rules_doc`(`doc_id`) ON DELETE RESTRICT  
  *(the battle profiles release used when building/calculating points)*
- `faction_id` INTEGER NOT NULL REFERENCES `faction`(`faction_id`) ON DELETE RESTRICT
- `army_name` TEXT NOT NULL
- `army_description` TEXT NULL
- `points_limit` INTEGER NOT NULL CHECK (`points_limit` > 0)
- `points_total_cached` INTEGER NOT NULL DEFAULT 0 CHECK (`points_total_cached` >= 0)
- `created_at` TEXT NOT NULL
- `updated_at` TEXT NOT NULL
- UNIQUE(`user_id`, `army_name`)

### Table: `roster_army_of_renown`
Armies of Renown replace normal faction rules when selected. citeturn24view2

- `roster_id` INTEGER PRIMARY KEY REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE RESTRICT  
  *(must be `kind='army_of_renown'` in application logic)*
- `notes` TEXT NULL

### Table: `roster_regiment`
A roster can include multiple regiments; each is led by a HERO, and the general’s regiment has expanded capacity. citeturn19view0turn19view1turn22view0

- `regiment_id` INTEGER PRIMARY KEY
- `roster_id` INTEGER NOT NULL REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `regiment_index` INTEGER NOT NULL CHECK (`regiment_index` >= 1)
- `name` TEXT NULL
- `commander_roster_unit_id` INTEGER NULL REFERENCES `roster_unit`(`roster_unit_id`) ON DELETE SET NULL
- UNIQUE(`roster_id`, `regiment_index`)

### Table: `roster_unit`
The “specific definition” / instance that appears in the saved roster.

Key requirements covered here:
- Link to the unit’s generic identity and its warscroll version.
- Record reinforcement state and model count.
- Record points snapshot (because points sources update). citeturn19view2turn22view1turn8view0
- Indicate whether it’s in a regiment, auxiliary, or regiment-of-renown slot. citeturn20view2turn20view1

- `roster_unit_id` INTEGER PRIMARY KEY
- `roster_id` INTEGER NOT NULL REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `unit_id` INTEGER NOT NULL REFERENCES `unit`(`unit_id`) ON DELETE RESTRICT
- `unit_warscroll_id` INTEGER NOT NULL REFERENCES `unit_warscroll`(`unit_warscroll_id`) ON DELETE RESTRICT
- `battle_profile_unit_id` INTEGER NULL REFERENCES `battle_profile_unit`(`battle_profile_unit_id`) ON DELETE SET NULL
- `assignment_kind` TEXT NOT NULL CHECK (`assignment_kind` IN ('regiment','auxiliary','regiment_of_renown'))
- `regiment_id` INTEGER NULL REFERENCES `roster_regiment`(`regiment_id`) ON DELETE CASCADE
- `roster_ror_id` INTEGER NULL REFERENCES `roster_regiment_of_renown`(`roster_ror_id`) ON DELETE CASCADE
- `ror_unit_slot_id` INTEGER NULL REFERENCES `ror_unit_slot`(`ror_unit_slot_id`) ON DELETE SET NULL
- `is_reinforced` INTEGER NOT NULL DEFAULT 0 CHECK (`is_reinforced` IN (0,1))
- `model_count` INTEGER NOT NULL CHECK (`model_count` >= 1)
- `points_snapshot` INTEGER NOT NULL CHECK (`points_snapshot` >= 0)
- `is_general` INTEGER NOT NULL DEFAULT 0 CHECK (`is_general` IN (0,1))
- `notes` TEXT NULL
- `sort_order` INTEGER NULL
- CHECK (
  (`assignment_kind`='regiment' AND `regiment_id` IS NOT NULL AND `roster_ror_id` IS NULL)
  OR (`assignment_kind`='auxiliary' AND `regiment_id` IS NULL AND `roster_ror_id` IS NULL)
  OR (`assignment_kind`='regiment_of_renown' AND `roster_ror_id` IS NOT NULL AND `regiment_id` IS NULL)
)

### Table: `roster_regiment_of_renown`
Roster can include up to 1 Regiment of Renown (unless specified otherwise in notes—store future exceptions in data). citeturn20view1turn8view0

- `roster_ror_id` INTEGER PRIMARY KEY
- `roster_id` INTEGER NOT NULL UNIQUE REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `ror_id` INTEGER NOT NULL REFERENCES `regiment_of_renown`(`ror_id`) ON DELETE RESTRICT
- `points_snapshot` INTEGER NOT NULL CHECK (`points_snapshot` >= 0)
- `notes` TEXT NULL

### Table: `roster_battle_formation`
Roster selects at most one battle formation (if any). citeturn22view0turn19view1turn12view0

- `roster_id` INTEGER PRIMARY KEY REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE RESTRICT
- `faction_item_points_id` INTEGER NULL REFERENCES `faction_item_points`(`faction_item_points_id`) ON DELETE SET NULL
- `points_snapshot` INTEGER NOT NULL DEFAULT 0 CHECK (`points_snapshot` >= 0)

### Table: `roster_faction_terrain`
Faction terrain features can be added if available; they may have points. citeturn22view0turn22view1turn20view3

- `roster_id` INTEGER NOT NULL REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE RESTRICT
- `faction_item_points_id` INTEGER NULL REFERENCES `faction_item_points`(`faction_item_points_id`) ON DELETE SET NULL
- `points_snapshot` INTEGER NOT NULL DEFAULT 0 CHECK (`points_snapshot` >= 0)
- PRIMARY KEY (`roster_id`, `faction_item_id`)

### Table: `roster_lore_pick`
Roster can pick up to one each of spell, prayer, and manifestation lore. citeturn22view0turn22view1

- `roster_id` INTEGER NOT NULL REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `lore_type` TEXT NOT NULL CHECK (`lore_type` IN ('spell_lore','prayer_lore','manifestation_lore'))
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE RESTRICT
- `faction_item_points_id` INTEGER NULL REFERENCES `faction_item_points`(`faction_item_points_id`) ON DELETE SET NULL
- `points_snapshot` INTEGER NOT NULL DEFAULT 0 CHECK (`points_snapshot` >= 0)
- PRIMARY KEY (`roster_id`, `lore_type`)

### Table: `roster_enhancement_pick`
Enhancements: typically one from each enhancement table; cannot duplicate an enhancement; a unit cannot have more than one enhancement of the same type; UNIQUE units cannot receive enhancements; restrictions also apply to Regiments of Renown. citeturn19view3turn24view2turn20view1

- `roster_enhancement_id` INTEGER PRIMARY KEY
- `roster_id` INTEGER NOT NULL REFERENCES `roster`(`roster_id`) ON DELETE CASCADE
- `enhancement_type` TEXT NOT NULL CHECK (`enhancement_type` IN (
  'heroic_trait','artefact_of_power','other'
))
- `faction_item_id` INTEGER NOT NULL REFERENCES `faction_item`(`faction_item_id`) ON DELETE RESTRICT
- `faction_item_points_id` INTEGER NULL REFERENCES `faction_item_points`(`faction_item_points_id`) ON DELETE SET NULL
- `assigned_roster_unit_id` INTEGER NULL REFERENCES `roster_unit`(`roster_unit_id`) ON DELETE SET NULL
- `points_snapshot` INTEGER NOT NULL DEFAULT 0 CHECK (`points_snapshot` >= 0)
- UNIQUE(`roster_id`, `enhancement_type`)  
- UNIQUE(`roster_id`, `faction_item_id`)
- UNIQUE(`assigned_roster_unit_id`, `enhancement_type`)  *(enforces “no unit has 2 artefacts,” etc.)*

## Integrity constraints and validation strategy

Some rules can be enforced structurally in the DB; others require app-level validation because they depend on counts/sums across many rows.

### Enforce in the database (recommended)

- **Referential integrity** with `FOREIGN KEY` constraints, using `ON DELETE CASCADE` from roster → regiments/units/picks, so deleting a roster cleans up its dependent rows. citeturn17search0turn17search14  
- **Enum safety** via `CHECK` constraints (assignment kinds, lore types, enhancement types, boolean flags, etc.). citeturn17search2turn17search14  
- **Uniqueness** constraints for one-per-roster selections (battle formation: `PRIMARY KEY(roster_id)`, lores: `PRIMARY KEY(roster_id,lore_type)`, regiment of renown: `UNIQUE(roster_id)`). citeturn20view1turn22view0  
- **Enhancement uniqueness & per-unit uniqueness** via the `UNIQUE` constraints shown in `roster_enhancement_pick`. citeturn24view2turn19view3

### Enforce in application logic (or triggers)

These require aggregates and/or complex predicate evaluation:

- **Points validation**: “Total points must not exceed points limit” and “no more than half your points on a single unit” depend on summing all picks/units, and cross-row comparison. citeturn22view1turn17search2  
- **Regiment count**: at least 1 regiment, maximum 5 regiments. citeturn19view0turn17search2  
- **Regiment membership limits**: each regiment is 1 HERO commander + 0–3 followers, except the general’s regiment which allows 0–4 followers; “followers normally non-HERO unless the battle profile says otherwise.” citeturn19view0turn19view1turn15search1turn17search2  
- **Reinforcement legality**: cannot reinforce if unit size is 1, if battle profile says “cannot be reinforced,” or if the unit is UNIQUE. citeturn19view2turn20view0turn12view0  
- **General selection**: must pick a HERO leading a regiment; WARMASTER constraints; and Regiments of Renown units cannot be the general. citeturn19view1turn20view1  
- **Regiment-of-renown restrictions**: their units can’t use allied faction rules, enhancements, lores, etc. citeturn20view1turn8view0turn24view2  
- **Auxiliary units side-effects**: the “fewer auxiliaries” command point benefit is game-state relative to opponent; store auxiliary count but don’t try to enforce the resulting benefit inside the roster DB. citeturn20view2turn22view0

## Source notes and why this schema matches the rules ecosystem

This schema is designed around the way entity["company","Games Workshop","warhammer publisher"] distributes rules and ongoing balance updates through entity["organization","Warhammer Community","downloads and news site"], alongside community-compiled structured rules references (e.g., entity["organization","Wahapedia","warhammer rules fan site"]). citeturn3view0turn8view0turn26view0 The explicit separation of **warscroll content** from **battle profile points**, and the first-class modeling of **documents/versions**, directly supports the fact that battle profiles are updated and newer publications supersede older ones. citeturn22view1turn8view0