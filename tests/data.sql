-- Insert cars
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (1, 'Toyota', 'Camry', 2019, 'Gasoline', 20000);
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (1, 'Honda', 'Civic', 2020, 'Gasoline', 22000);
INSERT INTO car (owner_id, make, model, year, fuel_type, price) VALUES (1, 'Ford', 'Mustang', 2018, 'Gasoline', 26000);

-- Insert pictures
INSERT INTO picture (car_id, uri) VALUES (1, 'https://example.com/toyota_camry.jpg');
INSERT INTO picture (car_id, uri) VALUES (2, 'https://example.com/honda_civic.jpg');
INSERT INTO picture (car_id, uri) VALUES (3, 'https://example.com/ford_mustang.jpg');
