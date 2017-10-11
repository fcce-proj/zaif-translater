CREATE TABLE phrase(
    id SERIAL PRIMARY KEY,
    key_lang TEXT NOT NULL,
    ja TEXT NOT NULL,
    en TEXT NOT NULL,
    zh TEXT NOT NULL,
);