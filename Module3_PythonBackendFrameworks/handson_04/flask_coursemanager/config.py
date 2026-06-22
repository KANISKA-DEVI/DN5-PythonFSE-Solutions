import os

class Config:
    SECRET_KEY                  = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG                       = True
    SQLALCHEMY_DATABASE_URI     = 'sqlite:///coursemanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False