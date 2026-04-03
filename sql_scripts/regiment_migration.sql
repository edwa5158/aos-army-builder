PRAGMA foreign_keys = OFF;

CREATE TABLE "Regiment_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"army_id"	INTEGER NOT NULL,
	FOREIGN KEY("army_id") REFERENCES "Army"("id") ON UPDATE CASCADE
);

INSERT INTO Regiment_new (id, army_id)
SELECT r.id, r.army_id
FROM Regiment r;

DROP TABLE Regiment;
ALTER TABLE Regiment_new RENAME TO Regiment;

PRAGMA foreign_keys = ON;