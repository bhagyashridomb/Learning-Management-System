# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:moonsoul@localhost:3307/LMS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
