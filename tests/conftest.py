import os
import pytest

# Patch init_db to avoid overriding SQLALCHEMY_DATABASE_URI with production env in tests.
# We import the database module and replace its init_db with a test-friendly version
from flask import Flask
from app.database import db as _db
from app.user import bp as user_bp


@pytest.fixture(scope='session')
def _setup_env():
    # Ensure any environment variables that init_db might read don't break tests
    # (we'll override init_db itself below)
    os.environ.pop('DB_USERNAME', None)
    os.environ.pop('DB_PASSWORD', None)
    os.environ.pop('DB_HOST', None)
    os.environ.pop('DB_PORT', None)
    os.environ.pop('DB_NAME', None)
    yield


@pytest.fixture
def app(_setup_env):
    # build a minimal Flask app for testing that uses sqlite in-memory
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret'

    # initialize DB and register blueprint
    _db.init_app(app)
    app.register_blueprint(user_bp, url_prefix='/user')

    # create tables
    with app.app_context():
        _db.create_all()

    yield app

    # teardown - drop all tables
    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seeded_db(app):
    from app.models import College, Program, Student
    with app.app_context():
        # create a college, program and a student linked using explicit commits and queries
        _db.session.add(College(code='C01', name='Test College'))
        _db.session.commit()

        # fetch ids via ORM queries to avoid any attribute expiration issues
        college_id = _db.session.query(College.id).filter_by(code='C01').scalar()

        _db.session.add(Program(code='P01', name='Test Program', college_id=college_id))
        _db.session.commit()
        program_id = _db.session.query(Program.id).filter_by(code='P01').scalar()

        _db.session.add(Student(id_number='2025-0001', first_name='John', last_name='Doe', program_id=program_id, year=1, gender='M'))
        _db.session.commit()
        student_id = _db.session.query(Student.id).filter_by(id_number='2025-0001').scalar()

        return {'college_id': college_id, 'program_id': program_id, 'student_id': student_id}
