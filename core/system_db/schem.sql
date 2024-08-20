CREATE TABLE IF NOT EXISTS person(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) UNIQUE NOT NULL,
    hash_password TEXT NOT NULL,
    email VARCHAR(90) UNIQUE NOT NULL,
    is_owner BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS connect_token(
    id SERIAL PRIMARY KEY,
    owner_id INTEGER UNIQUE NOT NULL,
    token TEXT UNIQUE NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES person(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS tracker_info(
    id SERIAL PRIMARY KEY,
    person_id INTEGER UNIQUE NOT NULL,
    "when" DATE NOT NULL,
    "start" TIMESTAMP NOT NULL,
    "end" TIMESTAMP NOT NULL
);