PRAGMA foreign_keys = OFF;

CREATE TABLE "Keyword_new" (
	"id"	INTEGER PRIMARY KEY NOT NULL,
	"name"	TEXT NOT NULL UNIQUE
);

INSERT INTO Keyword_new ([id], [name])
SELECT kw.[id], kw.[name]
FROM Keyword kw;

DROP TABLE Keyword;
ALTER TABLE Keyword_new RENAME TO Keyword;

PRAGMA foreign_keys = ON;