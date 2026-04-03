PRAGMA foreign_keys = OFF;
CREATE TABLE BattleProfile_new (
    id INTEGER PRIMARY KEY NOT NULL,
	"unit_size"	INTEGER,
	"points"	INTEGER,
	"can_be_reinforced"	INTEGER,
	"base_size"	TEXT,
    FOREIGN KEY (id) REFERENCES Warscroll(id) ON UPDATE CASCADE
);

INSERT INTO BattleProfile_new (id, unit_size, points, can_be_reinforced, base_size)
SELECT bp.id, bp.unit_size, bp.points, bp.can_be_reinforced, bp.base_size
FROM BattleProfile bp;

DROP TABLE BattleProfile;
ALTER TABLE BattleProfile_new RENAME TO BattleProfile;

PRAGMA foreign_keys = ON;