CREATE TYPE POSITION_PERSON AS ENUM ('frontend', 'backend', 'fullstack');

CREATE TABLE IF NOT EXISTS person(
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) UNIQUE NOT NULL,
    hash_password TEXT NOT NULL,
    email VARCHAR(90) UNIQUE NOT NULL,
    is_owner BOOLEAN NOT NULL,
    position POSITION_PERSON DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS project(
    id SERIAL PRIMARY KEY,
    token UUID UNIQUE NOT NULL,
    title VARCHAR(40) NOT NULL,
    "description" VARCHAR(800),
    "owner" INTEGER NOT NULL,
    date_create DATE NOT NULL,
    FOREIGN KEY("owner") REFERENCES person(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tracker_link(
    token UUID NOT NULL,
    worker INTEGER NOT NULL,
    FOREIGN KEY (worker) REFERENCES person(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (token) REFERENCES project(token)
    ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (token,worker)
);


CREATE TABLE IF NOT EXISTS tracker_info(
    id SERIAL PRIMARY KEY,
    person INTEGER NOT NULL,
    token UUID NOT NULL,
    "when" DATE NOT NULL,
    "time" TIME,
    is_active BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (person) REFERENCES person(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (token) REFERENCES project(token)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT u_token_worker UNIQUE(token,person)
);