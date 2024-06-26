import os
import logging
from flask import Flask, send_from_directory
from dotenv import load_dotenv

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object('flaskr.config.DevelopmentConfig')
        app.config.from_pyfile('config.py', silent=True)
        app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError as e:
        app.logger.error(f"Failed to create directories: {e}")

    # Initialize database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import car
    app.register_blueprint(car.bp)
    app.add_url_rule('/', endpoint='index')

    # Route for serving uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app