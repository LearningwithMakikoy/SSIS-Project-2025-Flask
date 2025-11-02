"""User blueprint routes."""
from flask import render_template, redirect, url_for, flash, request

# import the blueprint object from this package
from . import bp

# local imports
from .forms import StudentForm, ProgramForm, CollegeForm
from app.models import Student, Program, College
from app.database import db
from sqlalchemy.exc import IntegrityError


@bp.route('/')
def index():
    # templates are in app/templates/layouts/
    return render_template('layouts/index.html')


@bp.route('/programs', methods=['GET', 'POST'])
def programs():
    form = ProgramForm()
    # populate college choices for the program form
    colleges = College.query.order_by(College.name).all()
    form.college_id.choices = [(c.id, f"{c.code} - {c.name}") for c in colleges]

    if form.validate_on_submit():
        p = Program(code=form.code.data.strip(), name=form.name.data.strip(), college_id=form.college_id.data)
        db.session.add(p)
        try:
            db.session.commit()
            flash('Program created', 'success')
            return redirect(url_for('user.programs'))
        except IntegrityError:
            db.session.rollback()
            flash('Program code must be unique.', 'danger')

    programs = Program.query.order_by(Program.name).all()
    return render_template('layouts/programs.html', form=form, programs=programs, colleges=colleges)


@bp.route('/colleges', methods=['GET', 'POST'])
def colleges():
    form = CollegeForm()
    if form.validate_on_submit():
        c = College(code=form.code.data.strip(), name=form.name.data.strip())
        db.session.add(c)
        try:
            db.session.commit()
            flash('College created', 'success')
            return redirect(url_for('user.colleges'))
        except IntegrityError:
            db.session.rollback()
            flash('College code must be unique.', 'danger')

    colleges = College.query.order_by(College.name).all()
    return render_template('layouts/colleges.html', form=form, colleges=colleges)


@bp.route('/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()
    # populate program choices for the select field
    programs = Program.query.order_by(Program.name).all()
    form.program_id.choices = [(p.id, f"{p.code} - {p.name}") for p in programs]

    if form.validate_on_submit():
        new_student = Student(
            id_number=form.id_number.data.strip(),
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            program_id=form.program_id.data,
            year=form.year.data,
            gender=form.gender.data,
        )
        db.session.add(new_student)
        db.session.commit()
        flash('New student added successfully!', 'success')
        return redirect(url_for('user.students'))

    students = Student.query.all()
    return render_template('layouts/students.html', form=form, students=students, programs=programs)

