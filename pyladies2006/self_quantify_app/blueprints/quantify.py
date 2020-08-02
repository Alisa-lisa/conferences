from self_quantify_app.blueprints import api
from self_quantify_app.storage import db
import logging
from flask import redirect, render_template

logger = logging.getLogger(__name__)


@api.route("/quantify", methods=["POST", "GET"])
def quantify():
    """ 
    Mastery/Fun/Chore tracking form to 
    determine work-ife balance and assess 
    stress levels 
    """
    return render_template("worklife.html")
