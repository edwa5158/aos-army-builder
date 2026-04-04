CREATE TABLE Timing (
    [id] INTEGER NOT NULL,
    [name] TEXT UNIQUE NOT NULL,
    [phase] TEXT CHECK ([phase] IN (
        'Deployment Phase', 
        'Start of Battle Round', 
        'Start of Turn', 
        'Hero Phase', 
        'Movement Phase', 
        'Shooting Phase', 
        'Charge Phase', 
        'Combat Phase', 
        'End of Turn'
        )),
    [once_per] TEXT
);

CREATE TABLE Ability (
	[id] INTEGER PRIMARY KEY NOT NULL,
	[name] TEXT NOT NULL,
    [desc] TEXT NOT NULL,
    [timing_id] INTEGER NOT NULL,
    [declare] TEXT,
    [effect] TEXT,
    FOREIGN KEY ("timing_id") REFERENCES "timing"("id") ON UPDATE CASCADE
);

CREATE TABLE AbilityKeywords (
	[ability_id] INTEGER NOT NULL,
	[keyword_id] INTEGER NOT NULL,
	FOREIGN KEY ("ability_id") REFERENCES "ability"("id") ON UPDATE CASCADE,
	FOREIGN KEY ("keyword_id") REFERENCES "keyword"("id") ON UPDATE CASCADE,
	PRIMARY KEY ("ability_id", "keyword_id")
);

CREATE TABLE Spell (
	[id] INTEGER PRIMARY KEY NOT NULL,
	[casting_value] INTEGER NOT NULL,
	FOREIGN KEY ("id") REFERENCES "Ability"("id") ON UPDATE CASCADE
);

CREATE TABLE RoR (
	[id] INTEGER PRIMARY KEY NOT NULL,
	[name] TEXT NOT NULL,
	[points] INTEGER NOT NULL
	[desc] TEXT
);

CREATE TABLE Faction (
	[id] INTEGER PRIMARY KEY NOT NULL
	[name] TEXT NOT NULL
);

CREATE TABLE RoRIncl (
	[ror_id] INTEGER NOT NULL,
	[faction_id] INTEGER NOT NULL,
	FOREIGN KEY ("ror_id") REFERENCES "RoR"("id") ON UPDATE CASCADE,
	FOREIGN KEY ("faction_id") REFERENCES "Faction"("id") ON UPDATE CASCADE,
	PRIMARY KEY("ror_id", "faction_id")
);

CREATE TABLE RoROrg (
	[ror_id] INTEGER NOT NULL,
	[warscroll_id] INTEGER NOT NULL,
	[qty] INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY ("ror_id") REFERENCES "RoR"("id") ON UPDATE CASCADE,
	FOREIGN KEY ("warscroll_id") REFERENCES "Warscroll"("id") ON UPDATE CASCADE,
	PRIMARY KEY ("ror_id", "warscroll_id")
);

CREATE TABLE RoRAbilities (
	[ror_id] INTEGER NOT NULL,
	[ability_id] INTEGER NOT NULL,
	FOREIGN KEY ("ror_id") REFERENCES "RoR"("id") ON UPDATE CASCADE,
	FOREIGN KEY ("ability_id") REFERENCES "Ability"("id") ON UPDATE CASCADE
);