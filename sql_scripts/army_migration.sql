PRAGMA foreign_keys = OFF;

CREATE TABLE "Army_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT NOT NULL UNIQUE
);

INSERT INTO Army_new ([id], [name])
SELECT a.[id], a.[name]
FROM Army a;

DROP TABLE Army;
ALTER TABLE Army_new RENAME TO Army;

PRAGMA foreign_keys = ON;