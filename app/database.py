# app/database.py
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', 5432)
    name = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

