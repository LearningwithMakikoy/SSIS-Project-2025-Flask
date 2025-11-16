from .database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Student (db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    # formatted student identifier (example: "2023-1231")
    id_number = db.Column(db.String(50), unique=True, nullable=False)
    # split name fields
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    # year of study (1,2,3,4...), use Integer for numeric year
    year = db.Column(db.Integer)
    # link to Program table (course/program)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    program = db.relationship('Program', backref='students', lazy=True)

class Program(db.Model):
    __tablename__ = 'program'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)

class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    programs = db.relationship('Program', backref='college', lazy=True)