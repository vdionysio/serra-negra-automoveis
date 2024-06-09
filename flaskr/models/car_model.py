import os

from flask import current_app
from flaskr.db import get_db

def get_cars():
    db = get_db()
    rows = db.execute('''
        SELECT 
            car.id, car.owner_id, car.make, car.model, car.year, car.fuel_type, car.price, GROUP_CONCAT(picture.uri) as pictures
        FROM 
            car
        LEFT JOIN 
            picture ON car.id = picture.car_id
        GROUP BY
            car.id
        LIMIT 5;
    ''').fetchall()

    cars = []
    for row in rows:
        pictures = row[7].split(',') if row[7] else []
        cars.append({
            'id': row[0],
            'owner_id': row[1],
            'make': row[2],
            'model': row[3],
            'year': row[4],
            'fuel_type': row[5],
            'price': row[6],
            'pictures': pictures
        })

    return cars

def create_car(make, model, year, fuel_type, price, user_id, pictures):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO car (make, model, year, fuel_type, price, owner_id)'
        'VALUES (?, ?, ?, ?, ?, ?)',
        (make, model, year, fuel_type, price, user_id)
    )

    if pictures:
        car_id = cursor.lastrowid
        picname_list = save_pictures(pictures, car_id)
        
        sql = 'INSERT INTO picture (car_id, uri) VALUES (?, ?)'
        values = [(car_id, pic_name) for pic_name in picname_list]
        db.executemany(sql, values)
    db.commit()

def save_pictures(pictures, car_id):
    for pic in pictures:
        print(type(pic.filename))
        if not allowed_file(pic.filename):
            raise TypeError("Formato inválido. Os formatos aceitos são png, jpg, jpeg, gif.")

    picname_list = []
    for i in range(len(pictures)):
        ext = pictures[i].filename.rsplit('.', 1)[1].lower()
        pic_name = f'{car_id}_{i}.{ext}'
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
        pictures[i].save(path)
        picname_list.append(pic_name)

    return picname_list

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']