import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'),
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    )
    print(os.path.join(app.instance_path, 'flaskr.sqlite'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    from . import db

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import car
    app.register_blueprint(car.bp)
    app.add_url_rule('/', endpoint='index')

    return app