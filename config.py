from decouple import config
"""Global config Database and Flask"""

DATABASE_URI = config("DATABASE_URL")
if DATABASE_URI.startswith("sqlite://"):
    DATABASE_URI = DATABASE_URI.replace("sqlite://", "sqlite://", 1)

class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = config('SECRET_KEY', default='guess-me')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True