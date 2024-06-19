import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    DATABASE = os.path.join(os.environ.get('INSTANCE_PATH', 'instance'), 'flaskr.sqlite')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE = os.path.join(os.environ.get('INSTANCE_PATH', 'instance'), 'test_flaskr.sqlite')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
