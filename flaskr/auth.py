import functools
from sqlite3 import IntegrityError
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Constants
REQUIRED_FIELDS = ['username', 'password']

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        form_data = get_form_data(request.form, REQUIRED_FIELDS)
        error = validate_registration_form(form_data)

        if error is None:
            try:
                register_user(form_data['username'], form_data['password'])
                return redirect(url_for("auth.login"))
            except IntegrityError:
                error = f"User {form_data['username']} is already registered."

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        form_data = get_form_data(request.form, REQUIRED_FIELDS)
        error = validate_login_form(form_data)

        if error is None:
            user = get_user_by_username(form_data['username'])
            if user and check_password_hash(user['password'], form_data['password']):
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            else:
                error = 'Incorrect username or password.'

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = get_user_by_id(user_id) if user_id else None

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Helper functions
def get_form_data(form, fields):
    return {field: form.get(field) for field in fields}

def validate_registration_form(data):
    if not data['username']:
        return 'Username is required.'
    if not data['password']:
        return 'Password is required.'
    return None

def validate_login_form(data):
    if not data['username']:
        return 'Username is required.'
    if not data['password']:
        return 'Password is required.'
    return None

def register_user(username, password):
    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    db.commit()

def get_user_by_username(username):
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

def get_user_by_id(user_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
