# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes  # Import routes here

if __name__ == '__main__':
    app.run(debug=false)
