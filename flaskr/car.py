import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.models.car_model import get_cars, create_car

bp = Blueprint('car', __name__)

@bp.route('/')
def index():
    cars = get_cars()

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
        
        error = None

        variable_names = ['make', 'model', 'year', 'fuel_type', 'price']
        
        for var_name in variable_names:
            if locals()[var_name] is None:
                error = f'{var_name} é obrigatório.'
                break

        if error is not None:
            flash(error)
        else:
            create_car(make, model, year, fuel_type, price, g.user['id'], pictures)

            return redirect(url_for('car.index'))
    
    return render_template('car/create.html')

# def get_car(id):
