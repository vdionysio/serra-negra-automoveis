import os

from flask import current_app
from datetime import datetime
from flaskr.db import get_db

CAR_FIELDS = "car.id, car.owner_id, car.make, car.model, car.year, car.fuel_type, car.price"
CAR_PICTURES = "GROUP_CONCAT(picture.uri) as pictures"
CAR_JOIN = "LEFT JOIN picture ON car.id = picture.car_id"
CAR_GROUP_BY = "GROUP BY car.id"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_cars(limit=5):
    db = get_db()
    query = f'''
        SELECT {CAR_FIELDS}, {CAR_PICTURES}
        FROM car
        {CAR_JOIN}
        {CAR_GROUP_BY}
        LIMIT ?;
    '''
    rows = db.execute(query, (limit,)).fetchall()
    return list(map(row_to_car, rows))

def get_car(car_id):
    db = get_db()
    query = f'''
        SELECT {CAR_FIELDS}, {CAR_PICTURES}
        FROM car
        {CAR_JOIN}
        WHERE car.id = ?
        {CAR_GROUP_BY};
    '''
    row = db.execute(query, (car_id,)).fetchone()
    return row_to_car(row) if row else None

def create_car(make, model, year, fuel_type, price, user_id, pictures):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''
        INSERT INTO car (make, model, year, fuel_type, price, owner_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (make, model, year, fuel_type, price, user_id)
    )
    car_id = cursor.lastrowid

    if pictures and pictures[0].filename != '':
        picname_list = save_pictures(pictures, car_id)
        insert_pictures(db, car_id, picname_list)
    db.commit()

def edit_car(make, model, year, fuel_type, price, pictures, car_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''
        UPDATE car
        SET make = ?, model = ?, year = ?, fuel_type = ?, price = ?
        WHERE id = ?
        ''', (make, model, year, fuel_type, price, car_id)
    )
    if pictures and pictures[0].filename != '':
        picname_list = save_pictures(pictures, car_id)
        insert_pictures(db, car_id, picname_list)
    db.commit()

def delete_car(car_id):
    car = get_car(car_id)
    if car:
        db = get_db()
        delete_images([pic for pic in car['pictures']])
        db.execute('DELETE FROM car WHERE id = ?', (car_id,))
        db.commit()
        return True
    return False

def save_pictures(pictures, car_id):
    picname_list = []
    for i, pic in enumerate(pictures):
        if not allowed_file(pic.filename):
            raise TypeError("Invalid file format. Accepted formats are png, jpg, jpeg, gif.")
        ext = pic.filename.rsplit('.', 1)[1].lower()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pic_name = f'{car_id}_{timestamp}_{i}.{ext}'
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
        pic.save(path)
        picname_list.append(pic_name)
    return picname_list

def insert_pictures(db, car_id, picname_list):
    sql = 'INSERT INTO picture (car_id, uri) VALUES (?, ?)'
    values = [(car_id, pic_name) for pic_name in picname_list]
    db.executemany(sql, values)

def delete_images(images):
    db = get_db()
    for image in images:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            raise FileNotFoundError(f"File {image_path} does not exist")
        db.execute('DELETE FROM picture WHERE uri = ?', (image,))
    db.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def row_to_car(row):
    pictures = row['pictures'].split(',') if row['pictures'] else []
    return {
        'id': row['id'],
        'owner_id': row['owner_id'],
        'make': row['make'],
        'model': row['model'],
        'year': row['year'],
        'fuel_type': row['fuel_type'],
        'price': row['price'],
        'pictures': pictures
    }