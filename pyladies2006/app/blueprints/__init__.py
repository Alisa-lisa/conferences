from flask import Blueprint

api = Blueprint('api', __name__,
                        template_folder='templates')

from blueprints.user import *
