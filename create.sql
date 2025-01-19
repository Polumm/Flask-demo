CREATE TABLE upload (
    id SERIAL PRIMARY KEY,
    text VARCHAR(500) NOT NULL,
    image_data BYTEA NOT NULL
);
