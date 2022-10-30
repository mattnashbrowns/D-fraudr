DROP TABLE IF EXISTS datasets;
DROP TABLE IF EXISTS df_datafiles;

CREATE TABLE df_datafiles (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    description TEXT,
    md5sum TEXT
);

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    file_id INTEGER REFERENCES df_datafiles (id),
    column_id INTEGER,
    description TEXT,
    elements REAL[],
    base INTEGER,
    digits INTEGER[]
);

