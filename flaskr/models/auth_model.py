from flaskr.db import get_db
from werkzeug.security import generate_password_hash

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
