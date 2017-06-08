CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    adress TEXT NOT NULL,
    password_hash TEXT NOT NULL,
);
