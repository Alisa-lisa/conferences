from flask import Blueprint

api = Blueprint('api', __name__,
                        template_folder='templates')

from blueprints.user import *
from blueprints.quantify import *
from blueprints.admin import *
