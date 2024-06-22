-- Insert users
INSERT INTO user (username, password) VALUES ('user1', 'pbkdf2:sha256:600000$abcdef$1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef');
INSERT INTO user (username, password) VALUES ('user2', 'pbkdf2:sha256:600000$ghijkl$abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef');
INSERT INTO user (username, password) VALUES ('user3', 'pbkdf2:sha256:600000$mnopqr$abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef');

-- Insert cars
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (1, 'Toyota', 'Camry', 2019, 'Gasoline', 20000);
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (2, 'Honda', 'Civic', 2020, 'Gasoline', 22000);
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (3, 'Ford', 'Mustang', 2018, 'Gasoline', 26000);

-- Insert pictures
INSERT INTO picture (car_id, uri) VALUES (1, 'https://example.com/toyota_camry.jpg');
INSERT INTO picture (car_id, uri) VALUES (2, 'https://example.com/honda_civic.jpg');
INSERT INTO picture (car_id, uri) VALUES (3, 'https://example.com/ford_mustang.jpg');
