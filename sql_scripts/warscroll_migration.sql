PRAGMA foreign_keys = OFF;

CREATE TABLE Warscroll_new (
    id INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT UNIQUE NOT NULL,
	"move"	INTEGER,
	"save"	INTEGER,
	"control"	INTEGER,
	"health"	INTEGER,
	"url"	TEXT,
	"lore"	TEXT
);

INSERT INTO Warscroll_new (id, name, move, save, control, health, url, lore)
SELECT ws.[id], ws.[name], ws.[move], ws.[save], ws.[control], ws.[health], ws.[url], ws.[lore]
FROM Warscroll ws;

DROP TABLE Warscroll;
ALTER TABLE Warscroll_new RENAME TO Warscroll;

PRAGMA foreign_keys = ON;