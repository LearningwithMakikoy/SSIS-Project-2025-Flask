from flask import Blueprint

# create the blueprint
bp = Blueprint('user', __name__, template_folder='templates')

# import routes (controller will import `bp` from this package)
from . import controller  # noqa: E402 (import after bp)