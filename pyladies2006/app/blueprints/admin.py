""" admin API to gather data """
from blueprints import api
from flask import request, session, jsonify
from storage import db
from storage.user import User
from storage.quantify import Quantify

"""
flow:
    when registered you can get data with start and end dates
    delete all data for the user
    delee the user
"""

@api.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if 'user' in session:
        usr = db.session.query(User)\
                .filter(User.current_auth_token == session['user'])\
                .first()

        if request.method == "POST":
            if request.form['btn'] == "download":
                try:
                    start = request.form['start']
                    end = request.form['end']
                    # TODO: download as file to the system
                    results = db.ses.query(Quantify)\
                            .filter(Quantify.usr_id == usr.id)\
                            .filter(Quantify.timestamp >= start)\
                            .filter(Quantify.timestamp < end)
                            .all()
                    print(jsonify(results))
                    return jsonify(results)



