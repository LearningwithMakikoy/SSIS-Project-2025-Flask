"""User blueprint routes."""
from flask import render_template

# import the blueprint object from this package
from . import bp


@bp.route('/')
def index():
    # templates are in app/templates/layouts/
    return render_template('layouts/index.html')


@bp.route('/programs')
def programs():
    return render_template('layouts/programs.html')
