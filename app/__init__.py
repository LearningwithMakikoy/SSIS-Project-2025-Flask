from flask import Flask
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
        return app.send_static_file('index.html') if False else ("<p>Go to <a href='/user/'>/user/</a></p>")

    return app
