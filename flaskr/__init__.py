import os
from flask import Flask, send_from_directory

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads'),
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])

    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import car
    app.register_blueprint(car.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app