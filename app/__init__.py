from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from .database import db, init_db
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env if present

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://localhost/flaskdemo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    init_db(app)
    migrate = Migrate(app, db)

    # auth
    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
    from .user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # root route
    @app.route('/')
    def home():
        # app.send_static_file serves files from the static folder (not templates).
        # The earlier placeholder returned a plain string so no template was rendered.
        # Render the template located at app/templates/layouts/index.html instead.
        return render_template('layouts/index.html')

    return app
