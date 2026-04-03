PRAGMA foreign_keys = OFF;

CREATE TABLE "WeaponProfileAbility_new" (
	"weapon_profile_id"	INTEGER NOT NULL,
	"weapon_ability_id"	INTEGER NOT NULL,
	FOREIGN KEY("weapon_ability_id") REFERENCES "WeaponAbility"("id") ON UPDATE CASCADE,
	FOREIGN KEY("weapon_profile_id") REFERENCES "WeaponProfile"("id") ON UPDATE CASCADE,
	PRIMARY KEY("weapon_profile_id","weapon_ability_id")
);

INSERT INTO WeaponProfileAbility_new (weapon_profile_id, weapon_ability_id)
SELECT wpa.weapon_profile_id, wpa.weapon_ability_id
FROM WeaponProfileAbility wpa;

DROP TABLE WeaponProfileAbility;
ALTER TABLE WeaponProfileAbility_new RENAME TO WeaponProfileAbility; 

PRAGMA foreign_keys = ON;