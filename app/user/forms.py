from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp


class ProgramForm(FlaskForm):
	"""Form for creating / editing a Program.

	Note: set `form.college_id.choices = [(c.id, c.name) for c in colleges]` in the view
	before validating/rendering so the select displays available colleges.
	"""
	id = HiddenField('id')
	code = StringField('Code', validators=[DataRequired(), Length(max=10)])
	name = StringField('Name', validators=[DataRequired(), Length(max=100)])
	# choices must be populated by the view: form.college_id.choices = [(id, name), ...]
	college_id = SelectField('College', coerce=int, validators=[DataRequired()])
	submit = SubmitField('Save')


class CollegeForm(FlaskForm):
	"""Form for creating / editing a College."""
	id = HiddenField('id')
	code = StringField('Code', validators=[DataRequired(), Length(max=10)])
	name = StringField('Name', validators=[DataRequired(), Length(max=100)])
	submit = SubmitField('Save')


class StudentForm(FlaskForm):
		"""Form for creating / editing a Student.

		Fields:
			- id_number: formatted student ID (YYYY-NNNN), validated by regex
			- first_name, last_name: split names
			- program_id: populated by the view with available programs
			- year: year of study (1..n)
			- gender: simple select

		Usage:
			form = StudentForm()
			form.program_id.choices = [(p.id, p.name) for p in Program.query.order_by(Program.name).all()]
		"""
		id = HiddenField('id')
		id_number = StringField('Student ID', validators=[DataRequired(), Length(max=50),
																	 Regexp(r'^\d{4}-\d{4}$', message='Use format YYYY-NNNN')])
		first_name = StringField('First name', validators=[DataRequired(), Length(max=100)])
		last_name = StringField('Last name', validators=[DataRequired(), Length(max=100)])
		# populate choices in the view: form.program_id.choices = [(id, name), ...]
		program_id = SelectField('Program', coerce=int, validators=[DataRequired()])
		# year as a small select; adjust choices if you support more years
		year = SelectField('Year', coerce=int, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], validators=[DataRequired()])
		gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
		submit = SubmitField('Save')

