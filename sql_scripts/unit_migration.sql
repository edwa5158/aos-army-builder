PRAGMA foreign_keys = OFF;

CREATE TABLE "Unit_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"regiment_id"	INTEGER NOT NULL,
	"warscroll_id"	INTEGER NOT NULL,
	FOREIGN KEY("warscroll_id") REFERENCES "Warscroll"("id") ON UPDATE CASCADE,
	FOREIGN KEY("regiment_id") REFERENCES "Regiment"("id") ON UPDATE CASCADE
);

INSERT INTO Unit_new ([id], [regiment_id], [warscroll_id])
SELECT u.[id], u.[regiment_id], u.[warscroll_id]
FROM Unit u;

DROP TABLE Unit;
ALTER TABLE Unit_new RENAME TO Unit;

PRAGMA foreign_keys = ON;