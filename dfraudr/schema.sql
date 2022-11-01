DROP TABLE IF EXISTS df_datafiles;

CREATE TABLE df_datafiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    description TEXT,
    md5sum TEXT UNIQUE
);
