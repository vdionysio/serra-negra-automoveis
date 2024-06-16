import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)

from flaskr.auth import login_required
from flaskr.models.car_model import (
    get_cars, create_car, get_car, delete_images, edit_car, delete_car
)

bp = Blueprint('car', __name__)

@bp.route('/')
def index():
    cars = get_cars()

    return render_template('car/index.html', cars=cars)

@bp.route('/car/<int:car_id>')
def car_details(car_id):
    car = get_car(car_id)
    if car is None:
        abort(404, f'Carro de id {car_id} não encontrado')

    return render_template('car/car_details.html', car=car)

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

@bp.route('/car/<int:car_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(car_id):
    car = get_car(car_id)
    if request.method == 'POST':
        if car is None:
            abort(404, f'Carro de id {car_id} não encontrado')

        images = request.form.getlist('images')
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        fuel_type = request.form['fuel_type']
        price = request.form['price']
        pictures = request.files.getlist('pictures')

        if images:
            print(images)
            delete_images(images)

        edit_car(make, model, year, fuel_type, price, pictures, car_id)

        return redirect(url_for('car.car_details', car_id=car_id))

        
    return render_template('car/car_edit.html', car=car)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    delete_car(id)
    return redirect(url_for('car.index'))