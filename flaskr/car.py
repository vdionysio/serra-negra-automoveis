import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, abort
from flaskr.auth import login_required
from flaskr.models.car_model import get_cars, create_car, get_car, delete_images, edit_car, delete_car

bp = Blueprint('car', __name__)

REQUIRED_FIELDS = ['make', 'model', 'year', 'fuel_type', 'price']

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

@bp.route('/car/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        form_data = get_form_data(request.form, REQUIRED_FIELDS)
        pictures = request.files.getlist('pictures')

        error = validate_form_data(form_data)
        if error is not None:
            flash(error)
        else:
            create_car(**form_data, user_id=g.user['id'], pictures=pictures)
            return redirect(url_for('car.index'))
    
    return render_template('car/create.html')

@bp.route('/car/<int:car_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(car_id):
    car = get_car(car_id)
    if car is None:
        abort(404, f'Carro de id {car_id} não encontrado')

    if request.method == 'POST':
        form_data = get_form_data(request.form, REQUIRED_FIELDS)
        images_to_delete = request.form.getlist('images')
        pictures = request.files.getlist('pictures')

        if images_to_delete:
            delete_images(images_to_delete)

        edit_car(**form_data, pictures=pictures, car_id=car_id)
        return redirect(url_for('car.car_details', car_id=car_id))

    return render_template('car/car_edit.html', car=car)

@bp.route('/car/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    car = get_car(id)
    if car is None:
        abort(404, f'Carro de id {id} não encontrado')

    delete_car(id)
    return redirect(url_for('car.index'))

# Helper functions
def get_form_data(form, fields):
    return {field: form.get(field) for field in fields}

def validate_form_data(data):
    for field, value in data.items():
        if not value:
            return f'{field} é obrigatório.'
    return None