INSERT INTO Countries(id, name)
    VALUES(1, 'Argentina');

INSERT INTO States(id, name, country)
    VALUES(1, 'Ciudad Autónoma de Buenos Aires', 1);

INSERT INTO Cities(id, name, state)
    VALUES(1, 'Ciudad Autónoma de Buenos Aires', 1);

INSERT INTO Doc_Types(id, name)
    VALUES(1, 'LC/LE'), (2, 'DNI'), (3, 'Pasaporte');

INSERT INTO Sexes(id, name)
    VALUES(1, 'Femenino'), (2, 'Masculino'), (3, 'Otro');

INSERT INTO Positions(id, name)
    VALUES(1, 'Socio'), (2, 'Presidente'), (3, 'Secretario'), (4, 'Vocal');

INSERT INTO Addresses(id, address, city, phone)
    VALUES(1, 'Tuyutí 7126', 1, '1146414581');

INSERT INTO Persons(id, doc_type, doc_number, last_name, first_name, birthdate, sex, address, cellphone)
    VALUES(1, 2, 14009938, 'Córdoba', 'Adrián Esteban', '08-29-1960', 2, 1, '1157385359');


INSERT INTO Partners(id, person, partner_number, pami_number, incorporation, position)
    VALUES(1, 1, 234, '140307131409/00', '01-01-2026', 1);

INSERT INTO Events(id, name, date, creation, description, charge)
    VALUES(1, 'Cuota 2/2026', '02-01-2026', NOW(), 'Cuota febrero 2026', 3000);

INSERT INTO Share(id, event, partner)
    VALUES(1, 1, 1);

INSERT INTO Accounting(id, date, concept, description, credit)
    VALUES(1, '03-10-2026', 'Donación', 'Sociedad de Vecinos del Barrio de Liniers', 3000000);
