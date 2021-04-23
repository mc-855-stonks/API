import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'stonks'
DB_LOCAL_DEV_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, '{}_dev.db'.format(DB_NAME)))
DB_LOCAL_TEST_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, '{}_test.db'.format(DB_NAME)))

class FlaskAppConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    DEBUG = False

class DevelopmentConfig(FlaskAppConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', DB_LOCAL_DEV_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(FlaskAppConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_LOCAL_TEST_URI
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(FlaskAppConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', '')

config_by_env = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    qa=ProductionConfig
)

SECRET_KEY = FlaskAppConfig.SECRET_KEY

