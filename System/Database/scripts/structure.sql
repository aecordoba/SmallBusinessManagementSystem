DROP DATABASE IF EXISTS sbms;
DROP ROLE IF EXISTS sbmsapp;

-- -----------------------------------------------------
-- Database sbms
-- -----------------------------------------------------
CREATE DATABASE sbms;

-- -----------------------------------------------------
-- Role
-- -----------------------------------------------------
CREATE ROLE sbmsapp WITH LOGIN PASSWORD 'sbmsapp123';
GRANT ALL PRIVILEGES ON DATABASE sbms TO sbmsapp;

\c sbms

-- -----------------------------------------------------
-- Tables
-- -----------------------------------------------------

CREATE TABLE Countries(
    id SERIAL PRIMARY KEY,
    name VARCHAR(35) NOT NULL UNIQUE
);

CREATE TABLE States(
    id SERIAL PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    country INT NOT NULL,
    UNIQUE(name, country),
    CONSTRAINT fk_states_countries FOREIGN KEY (country) REFERENCES Countries(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Cities(
    id SERIAL PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    state INT NOT NULL,
    UNIQUE(name, state),
    CONSTRAINT fk_cities_states FOREIGN KEY (state) REFERENCES States(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


CREATE TABLE Addresses(
    id SERIAL PRIMARY KEY,
    address VARCHAR(30) NOT NULL,
    city INT NOT NULL,
    phone VARCHAR(10),
    CONSTRAINT fk_addresses_cities FOREIGN KEY (city) REFERENCES Cities(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TYPE genders AS ENUM ('male', 'female', 'other');

CREATE TYPE documents AS ENUM ('document_1', 'document_2', 'document_3'); -- 1- Soc. Security / 2- Drivers License / 3- Passport

CREATE TABLE Persons(
    id SERIAL PRIMARY KEY,
    doc_type documents NOT NULL DEFAULT 'document_1',
    doc_number INT NOT NULL,
    social_security VARCHAR(15) UNIQUE,
    last_name VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    email VARCHAR(50) CHECK (email ~* '^\S+@\S+\.\S+$'),
    birthdate DATE NOT NULL,
    gender genders NOT NULL,
    address INT NOT NULL,
    cellphone VARCHAR(10),
    UNIQUE(doc_type, doc_number),
    CONSTRAINT fk_persons_addresses FOREIGN KEY (address) REFERENCES Addresses(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TYPE positions AS ENUM ('position_1', 'position_2', 'position_3', 'position_4'); -- 1- associate / 2- president / 3- secretary / 4- member

CREATE TYPE status AS ENUM ('status_1', 'status_2', 'status_3'); -- 1- active / 2- life / 3- inactive

CREATE TABLE Partners(
    id SERIAL PRIMARY KEY,
    person INT NOT NULL,
    partner_number INT NOT NULL UNIQUE,
    incorporation DATE NOT NULL,
    position positions NOT NULL DEFAULT 'position_1',
    status status NOT NULL DEFAULT 'status_1',
    CONSTRAINT fk_partners_persons FOREIGN KEY (person) REFERENCES Persons(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Events(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    date DATE NOT NULL,
    time TIME,
    attendants INT,
    creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    charge NUMERIC(10,2),
    automatic BOOLEAN NOT NULL,
    UNIQUE(name, date, time)
);

CREATE TABLE Share(
    id SERIAL PRIMARY KEY,
    event INT NOT NULL,
    partner INT NOT NULL,
    attendees INT DEFAULT 1,
    payment NUMERIC(10,2) DEFAULT 0,
    UNIQUE(partner, event),
    CONSTRAINT fk_share_event FOREIGN KEY (event) REFERENCES Events(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_share_partners FOREIGN KEY (partner) REFERENCES Partners(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Accounting(
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    concept VARCHAR(30) NOT NULL,
    description TEXT,
    debit NUMERIC(15,2),
    credit NUMERIC(15,2)
);

CREATE TABLE News(
    id SERIAL PRIMARY KEY,
    event INT,
    edition TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    brief TEXT NOT NULL,
    description TEXT,
    CONSTRAINT fk_news_event FOREIGN KEY (event) REFERENCES Events(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);



GRANT ALL PRIVILEGES ON SCHEMA public TO sbmsapp;
GRANT ALL ON ALL TABLES IN SCHEMA public TO sbmsapp;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sbmsapp;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO sbmsapp;
