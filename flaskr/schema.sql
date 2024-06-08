DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS car;
DROP TABLE IF EXISTS picture;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    fuel_type TEXT NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE picture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    uri TEXT NOT NULL,
    FOREIGN KEY (car_id) REFERENCES car (id) ON DELETE CASCADE
);