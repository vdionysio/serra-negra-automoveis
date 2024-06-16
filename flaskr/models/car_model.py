import os

from flask import current_app
from datetime import datetime
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

    cars = map(row_to_car, rows)

    return cars

def get_car(car_id):
    db = get_db()
    row = db.execute('''
        SELECT 
            car.id, car.owner_id, car.make, car.model, car.year, car.fuel_type, car.price, GROUP_CONCAT(picture.uri) as pictures
        FROM 
            car
        LEFT JOIN 
            picture ON car.id = picture.car_id
        WHERE 
            car.id = ?
        GROUP BY
            car.id
    ''', (car_id,)).fetchone()
    
    return row_to_car(row)

def create_car(make, model, year, fuel_type, price, user_id, pictures):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO car (make, model, year, fuel_type, price, owner_id)'
        'VALUES (?, ?, ?, ?, ?, ?)',
        (make, model, year, fuel_type, price, user_id)
    )

    if pictures and pictures[0].filename != '':
        car_id = cursor.lastrowid
        picname_list = save_pictures(pictures, car_id)
        
        sql = 'INSERT INTO picture (car_id, uri) VALUES (?, ?)'
        values = [(car_id, pic_name) for pic_name in picname_list]
        db.executemany(sql, values)
    db.commit()

def edit_car(make, model, year, fuel_type, price, pictures, car_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE car
        SET make = (?),
            model = (?),
            year = (?),
            fuel_type = (?),
            price = (?)
        WHERE
            id = (?)
    ''', (make, model, year, fuel_type, price, car_id)
    )
    
    if pictures and pictures[0].filename != '':
        print("PICTURES AQUI")
        print(pictures)
        picname_list = save_pictures(pictures, car_id)
        
        sql = 'INSERT INTO picture (car_id, uri) VALUES (?, ?)'
        values = [(car_id, pic_name) for pic_name in picname_list]
        db.executemany(sql, values)
    db.commit()

def save_pictures(pictures, car_id):
    for pic in pictures:
        if not allowed_file(pic.filename):
            raise TypeError("Formato inválido. Os formatos aceitos são png, jpg, jpeg, gif.")

    picname_list = []
    for i in range(len(pictures)):
        ext = pictures[i].filename.rsplit('.', 1)[1].lower()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pic_name = f'{car_id}_{timestamp}_{i}.{ext}'
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
        pictures[i].save(path)
        picname_list.append(pic_name)

    return picname_list

def delete_images(images):
    db = get_db()
    try:
        for image in images:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
            if os.path.exists(image_path):
                
                os.remove(image_path)
            else:
                raise FileNotFoundError(f"File {image_path} does not exist")
            db.execute('DELETE FROM picture WHERE uri = ?', (image,))

        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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

def delete_car(car_id):
    car = get_car(car_id)
    if car:
        db = get_db()
        rows = db.execute('SELECT uri FROM picture WHERE car_id = ?', (car_id,)).fetchall()
        pic_names = [row['uri'] for row in rows]
        for image in pic_names:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image)
            if os.path.exists(image_path):
                
                os.remove(image_path)
            else:
                raise FileNotFoundError(f"File {image_path} does not exist")
        db.execute('DELETE FROM car WHERE id = ?', (car_id,))
        db.commit()
        return True
    else:
        return False

def row_to_picture(row):
    return {
        'id': row['id'],
        'car_id': row['owner_id'],
        'uri': row['make'],
        'model': row['model'],
        'year': row['year'],
        'fuel_type': row['fuel_type'],
        'price': row['price'],
        'pictures': pictures
    }