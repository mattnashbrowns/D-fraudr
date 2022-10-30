DROP TABLE IF EXISTS datasets;

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    description TEXT,
    elements REAL[],
    base INTEGER,
    digits INTEGER[]
);