import os

class Config:
    # Secret key for security
    SECRET_KEY = 'mysecretkey123'

    # Database connection
    # This creates flask_course.db file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_course.db'

    # Don't track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Show debug errors
    DEBUG = True