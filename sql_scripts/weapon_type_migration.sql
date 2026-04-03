PRAGMA foreign_keys = OFF;

CREATE TABLE "WeaponType_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	"value" TEST NOT NULL UNIQUE
);

INSERT INTO WeaponType_new ([id], [name], [value])
SELECT wt.[id], wt.[name], wt.[value]
FROM WeaponType wt;

DROP TABLE WeaponType;
ALTER TABLE WeaponType_new RENAME TO WeaponType;

PRAGMA foreign_keys = ON;