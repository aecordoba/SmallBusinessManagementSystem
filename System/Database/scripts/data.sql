INSERT INTO Countries(id, name)
    VALUES(1, 'Argentina');

INSERT INTO States(id, name, country)
    VALUES(1, 'Ciudad Autónoma de Buenos Aires', 1);

INSERT INTO Cities(id, name, state)
    VALUES(1, 'Ciudad Autónoma de Buenos Aires', 1);

INSERT INTO Addresses(id, address, zip_code, city, phone)
    VALUES(1, 'Tuyutí 7126', '1408', 1, '1146414581');

INSERT INTO Persons(id, doc_type, doc_number, social_security, last_name, first_name, email, birthdate, gender, address, cellphone)
    VALUES(1, 'document_1', 14009938, '140307131409/00', 'Córdoba', 'Adrián Esteban', 'aecordoba@gmail.com', '08-29-1960', 'male', 1, '1157385359');

INSERT INTO Partners(id, person, partner_number, incorporation, position)
    VALUES(1, 1, 234, '01-01-2026', 'position_1');

INSERT INTO Events(id, name, date, time, attendants, creation, description, charge, automatic, validity)
    VALUES(1, 'Cuota 2/2026', '02-01-2026', NULL, NULL, NOW(), 'Cuota febrero 2026', 3000, true, 'monthly'),
    (2, 'Legislatura Porteña', '02-07-2026', '10:30', 30, NOW(), 'Visita a la Legislatura Porteña', NULL, false, null);

INSERT INTO Share(id, event, partner)
    VALUES(1, 1, 1);

INSERT INTO Accounting(id, date, concept, description, credit)
    VALUES(1, '03-10-2026', 'Donación', 'Sociedad de Vecinos del Barrio de Liniers', 3000000);

INSERT INTO News(id, event, edition, brief, description)
    VALUES(1, NULL, NOW(), 'Nuevo espacio para nuestros asociados.', 'La comisión directiva decidió disponer un nuevo espacio para usos múltiples de nuestros asociados. El nuevo sector podrá ser utiizado tanto por los asociados como sus invitados, con previa autorización.'),
    (2, 2, NOW(), 'Visita a la Legislatura Porteña.', 'Con motivo de celebrarse el vigésimo aniversario de la inauguración del edificio de la legislatura porteña, el Gobierno de la Ciudad invita a los asociados al Centro, a participar de la visita guiada que se realizará el 7 de mayo. Nos reuniremos ese día a las 10:30 hs. en el Centro. Les pedimos, puntualidad.');
