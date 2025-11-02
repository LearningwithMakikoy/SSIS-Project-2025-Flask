"""User blueprint routes."""
from flask import render_template, redirect, url_for, flash, request, jsonify

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
    # populate college choices for the program form (ORM objects)
    colleges_q = College.query.order_by(College.name).all()
    form.college_id.choices = [(c.id, f"{c.code} - {c.name}") for c in colleges_q]

    # handle create or edit
    if form.validate_on_submit():
        if form.id.data:
            # editing existing program
            prog = Program.query.get(int(form.id.data))
            if prog:
                prog.code = form.code.data.strip()
                prog.name = form.name.data.strip()
                prog.college_id = form.college_id.data
        else:
            prog = Program(code=form.code.data.strip(), name=form.name.data.strip(), college_id=form.college_id.data)
            db.session.add(prog)
        try:
            db.session.commit()
            flash('Program saved', 'success')
            return redirect(url_for('user.programs'))
        except IntegrityError:
            db.session.rollback()
            flash('Program code must be unique.', 'danger')

    # serializable lists for templates/JS
    programs_q = Program.query.order_by(Program.name).all()
    programs = [
        {'id': p.id, 'code': p.code, 'name': p.name, 'college': (p.college.name if p.college else ''), 'college_id': p.college_id}
        for p in programs_q
    ]
    colleges = [{'id': c.id, 'code': c.code, 'name': c.name} for c in colleges_q]

    return render_template('layouts/programs.html', form=form, programs=programs, colleges=colleges)


@bp.route('/colleges', methods=['GET', 'POST'])
def colleges():
    form = CollegeForm()
    if form.validate_on_submit():
        if form.id.data:
            col = College.query.get(int(form.id.data))
            if col:
                col.code = form.code.data.strip()
                col.name = form.name.data.strip()
        else:
            col = College(code=form.code.data.strip(), name=form.name.data.strip())
            db.session.add(col)
        try:
            db.session.commit()
            flash('College saved', 'success')
            return redirect(url_for('user.colleges'))
        except IntegrityError:
            db.session.rollback()
            flash('College code must be unique.', 'danger')

    colleges_q = College.query.order_by(College.name).all()
    colleges = [{'id': c.id, 'code': c.code, 'name': c.name} for c in colleges_q]
    return render_template('layouts/colleges.html', form=form, colleges=colleges)


@bp.route('/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()
    programs_q = Program.query.order_by(Program.name).all()
    form.program_id.choices = [(p.id, f"{p.code} - {p.name}") for p in programs_q]

    if form.validate_on_submit():
        if form.id.data:
            st = Student.query.get(int(form.id.data))
            if st:
                st.id_number = form.id_number.data.strip()
                st.first_name = form.first_name.data.strip()
                st.last_name = form.last_name.data.strip()
                st.program_id = form.program_id.data
                st.year = form.year.data
                st.gender = form.gender.data
        else:
            st = Student(
                id_number=form.id_number.data.strip(),
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                program_id=form.program_id.data,
                year=form.year.data,
                gender=form.gender.data,
            )
            db.session.add(st)
        db.session.commit()
        flash('Student saved', 'success')
        return redirect(url_for('user.students'))

    students_q = Student.query.all()
    students = [
        {
            'id': s.id,
            'id_number': s.id_number,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'program_id': s.program_id,
            'program': (s.program.name if s.program else ''),
            'year': s.year,
            'gender': s.gender,
        }
        for s in students_q
    ]
    programs = [{'id': p.id, 'code': p.code, 'name': p.name} for p in programs_q]
    return render_template('layouts/students.html', form=form, students=students, programs=programs)


@bp.route('/students/delete/<int:item_id>', methods=['POST'])
def delete_student(item_id):
    st = Student.query.get_or_404(item_id)
    try:
        db.session.delete(st)
        db.session.commit()
        return jsonify(success=True, message='Student deleted')
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 400


@bp.route('/programs/delete/<int:item_id>', methods=['POST'])
def delete_program(item_id):
    prog = Program.query.get_or_404(item_id)
    # prevent deleting programs that still have students
    if getattr(prog, 'students', None) and len(prog.students) > 0:
        return jsonify(success=False, message='Program cannot be deleted because students are enrolled.'), 400
    try:
        db.session.delete(prog)
        db.session.commit()
        return jsonify(success=True, message='Program deleted')
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 400


@bp.route('/colleges/delete/<int:item_id>', methods=['POST'])
def delete_college(item_id):
    col = College.query.get_or_404(item_id)
    # prevent deleting colleges that still have programs
    if getattr(col, 'programs', None) and len(col.programs) > 0:
        return jsonify(success=False, message='College cannot be deleted because programs are linked.'), 400
    try:
        db.session.delete(col)
        db.session.commit()
        return jsonify(success=True, message='College deleted')
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e)), 400

