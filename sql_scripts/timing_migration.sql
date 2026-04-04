-- CREATE TABLE Timing (
--     [id] INTEGER NOT NULL,
--     [name] TEXT UNIQUE NOT NULL,
--     [phase] TEXT CHECK ([phase] IN (
--         'Deployment Phase', 
--         'Start of Battle Round', 
--         'Start of Turn', 
--         'Hero Phase', 
--         'Movement Phase', 
--         'Shooting Phase', 
--         'Charge Phase', 
--         'Combat Phase', 
--         'End of Turn'
--         )),
--     [once_per] TEXT
-- );

PRAGMA foreign_keys = OFF;

CREATE TABLE "Timing_new" (
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
        'End of Turn',
        'End of Battle Round'
        )),
    [player] TEXT CHECK ([player] IN ('You', 'Enemy', 'Any')),
    [once_per] TEXT
);

INSERT INTO Timing_new ([id], [name], [phase], [player], [once_per])
SELECT t.[id], t.[name], t.[phase], t.[player], t.[once_per]
FROM Timing t;

DROP TABLE Timing;
ALTER TABLE Timing_new RENAME TO Timing;

PRAGMA foreign_keys = ON;