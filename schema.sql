DROP TABLE IF EXISTS persona;

CREATE TABLE persona(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [age] INTEGER NOT NULL,
    [nationality] TEXT NOT NULL
);