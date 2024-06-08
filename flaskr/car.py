import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('car', __name__)

@bp.route('/')
def index():
    db = get_db()
    cars = db.execute('''
        SELECT 
            car.id, car.owner_id, car.make, car.model, car.year, car.fuel_type, 
            car.price, 
            picture.id, picture.uri
        FROM car
        LEFT JOIN picture ON car.id = picture.car_id
    ''').fetchall()
    print(cars)
    return render_template('car/index.html', cars=cars)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        fuel_type = request.form['fuel_type']
        price = request.form['price']
        pictures = request.files.getlist('pictures')
        
        print(f'Pictures after upload {pictures}')
        error = None

        variable_names = ['make', 'model', 'year', 'fuel_type', 'price']
        
        for var_name in variable_names:
            if locals()[var_name] is None:
                error = f'{var_name} é obrigatório.'
                break

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO car (make, model, year, fuel_type, price, owner_id)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (make, model, year, fuel_type, price, g.user['id'])
            )
            if pictures:
                car_id = cursor.lastrowid
                path_list = save_pictures(pictures, car_id)
                
                sql = 'INSERT INTO picture (car_id, uri) VALUES (?, ?)'
                values = [(car_id, path) for path in path_list]
                db.executemany(sql, values)
            db.commit()
            return redirect(url_for('car.index'))
    
    return render_template('car/create.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_pictures(pictures, car_id):
    for pic in pictures:
        print(type(pic.filename))
        if not allowed_file(pic.filename):
            raise TypeError("Formato inválido. Os formatos aceitos são png, jpg, jpeg, gif.")

    path_list = []
    for i in range(len(pictures)):
        ext = pictures[i].filename.rsplit('.', 1)[1].lower()
        pic_name = f'{car_id}_{i}.{ext}'
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name)
        pictures[i].save(path)
        path_list.append(path)
        print(f'Saving {path}')

    return path_list