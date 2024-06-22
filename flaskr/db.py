import sqlite3
import click
from flask import current_app, g
import os

def get_db():
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            current_app.logger.error(f'Database connection error: {e}')
            raise
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        try:
            db.close()
        except sqlite3.Error as e:
            current_app.logger.error(f'Error closing the database: {e}')

def init_db():
    db = get_db()
    schema_path = os.path.join(current_app.root_path, 'schema.sql')
    try:
        with current_app.open_resource(schema_path) as f:
            db.executescript(f.read().decode('utf8'))
    except sqlite3.Error as e:
        current_app.logger.error(f"Error initializing the database: {e}")
        raise

@click.command('init-db')
def init_db_command():
    try:
        init_db()
        click.echo('Initialized the database')
    except Exception as e:
        click.echo(f"Failed to initialize the database: {e}")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)