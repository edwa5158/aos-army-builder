PRAGMA foreign_keys = OFF;
CREATE TABLE "WeaponProfile_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"warscroll_id" INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"attack"	INTEGER,
	"hit"	INTEGER,
	"wound"	INTEGER,
	"rend"	INTEGER,
	"damage"	INTEGER,
	"weapon_type_id"	INTEGER,
	"range"	TEXT,
	FOREIGN KEY("weapon_type_id") REFERENCES "WeaponType"("id") ON UPDATE CASCADE,
	FOREIGN KEY("warscroll_id") REFERENCES "Warscroll"("id") ON UPDATE CASCADE
);

INSERT INTO WeaponProfile_new ([id], [warscroll_id], [name], [attack], [hit], [wound], [rend], [damage], [weapon_type_id], [range])
SELECT wp.[id], wp.[warscroll_id], wp.[name], wp.[attack], wp.[hit], wp.[wound], wp.[rend], wp.[damage], wp.[weapon_type_id], wp.[range]
FROM WeaponProfile wp;

DROP TABLE WeaponProfile;
ALTER TABLE WeaponProfile_new RENAME TO WeaponProfile;

PRAGMA foreign_keys = ON;