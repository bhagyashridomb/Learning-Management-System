from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')  # Make sure your config is correct
db = SQLAlchemy(app)

from app import routes  # Import routes after creating app
