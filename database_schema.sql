CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    description VARCHAR(500),
    priority VARCHAR(50),
    status VARCHAR(50),
    created_date TIMESTAMP,
    user_id INTEGER REFERENCES "user"(id)
);