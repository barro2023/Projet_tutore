import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://barro:BARROBA@localhost/dbproject')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    

    
