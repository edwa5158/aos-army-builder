PRAGMA foreign_keys = OFF;

CREATE TABLE "WeaponAbility_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
    "description" TEXT
);

INSERT INTO WeaponAbility_new ([id], [name], [description])
SELECT wa.[id], wa.[name], wa.[description]
FROM WeaponAbility wa;

DROP TABLE WeaponAbility;
ALTER TABLE WeaponAbility_new RENAME TO WeaponAbility;

PRAGMA foreign_keys = ON;