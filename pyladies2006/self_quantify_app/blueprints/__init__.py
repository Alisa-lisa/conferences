""" collecting all routes/functionality together """
from flask import Blueprint


api = Blueprint("api", "quantify", template_folder="templates")
from .user import *
from .quantify import *
from .admin import *

