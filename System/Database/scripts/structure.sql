DROP DATABASE IF EXISTS sbms;
DROP ROLE IF EXISTS sbmsapp;

-- -----------------------------------------------------
-- Database liniers_sur
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
    name VARCHAR(35) NOT NULL
);

CREATE TABLE States(
    id SERIAL PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    country INT NOT NULL,
    CONSTRAINT fk_states_countries FOREIGN KEY (country) REFERENCES Countries(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Cities(
    id SERIAL PRIMARY KEY,
    name VARCHAR(35) NOT NULL,
    state INT NOT NULL,
    CONSTRAINT fk_cities_states FOREIGN KEY (state) REFERENCES States(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Positions(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE Doc_Types(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE Sexes(
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) NOT NULL
);

CREATE TABLE Addresses(
    id SERIAL PRIMARY KEY,
    address VARCHAR(30) NOT NULL,
    city INT NOT NULL,
    phone VARCHAR(10),
    CONSTRAINT fk_addresses_cities FOREIGN KEY (city) REFERENCES Cities(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Persons(
    id SERIAL PRIMARY KEY,
    doc_type INT NOT NULL,
    doc_number INT NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    birthdate DATE NOT NULL,
    sex INT NOT NULL,
    address INT NOT NULL,
    cellphone VARCHAR(10),
    CONSTRAINT fk_persons_doc_types FOREIGN KEY (doc_type) REFERENCES Doc_Types(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_persons_sexes FOREIGN KEY (sex) REFERENCES Sexes(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_persons_addresses FOREIGN KEY (address) REFERENCES Addresses(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Partners(
    id SERIAL PRIMARY KEY,
    person INT NOT NULL,
    partner_number INT NOT NULL,
    pami_number VARCHAR(15),
    incorporation DATE NOT NULL,
    position INT NOT NULL,
    CONSTRAINT fk_partners_persons FOREIGN KEY (person) REFERENCES Persons(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_partners_positions FOREIGN KEY (position) REFERENCES Positions(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Events(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    date DATE NOT NULL,
    time TIME,
    creation TIMESTAMP NOT NULL,
    description TEXT,
    charge NUMERIC(10,2)
);

CREATE TABLE Share(
    id SERIAL PRIMARY KEY,
    event INT NOT NULL,
    partner INT NOT NULL,
    attendees INT DEFAULT 1,
    payment NUMERIC(10,2) DEFAULT 0,
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

GRANT ALL ON ALL TABLES IN SCHEMA public TO sbmsapp;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sbmsapp;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO sbmsapp;
