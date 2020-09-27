""" admin API to gather data """
from blueprints import api
from flask import request, session, send_file, redirect, url_for, render_template
from storage import db
from storage.user import User
from storage.quantify import Quantify
import csv
import logging 
from dateutil.parser import *
import os

logger = logging.getLogger(__name__)
"""
flow:
    when registered you can get data with start and end dates - form/btn
    delete all data for the user - btn
    delete the user - btn
"""

@api.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if 'user' in session:
        usr = db.session.query(User)\
                .filter(User.current_auth_token == session['user'])\
                .filter(User.current_auth_token != None)\
                .first()
        logger.info(f"current user is id {usr.id}")
        if usr is not None:
            if request.method == "POST":
                if request.form['btn'] == "download":
                    try:
                        start = (request.form['start'])
                        end = (request.form['end'])
                        results = db.session.query(Quantify)\
                                .filter(Quantify.usr_id == usr.id)\
                                .filter(Quantify.timestamp >= start)\
                                .filter(Quantify.timestamp < end)\
                                .all()
                        with open("results.csv", 'w') as o:
                            writer = csv.writer(o)
                            for item in results:
                                writer.writerow(item.to_list())
                        return send_file("results.csv")
                    except Exception as ex:
                        print(f"can not collect data into file due to {ex}")
                        return render_template("admin.html")
                elif request.form["btn"] == "delete user":
                    try:
                        db.session.delete(usr)
                        db.session.commit()
                        return redirect(url_for("api.logout"))
                    except Exception as ex:
                        print(f"Could not delete user due to {ex}")
                        return render_template("admin.html")
                else:  # delete data for thi user
                    try:
                        db.session.query(Quantify).filter(Quantify.usr_id == usr.id).delete()
                        db.session.commit()
                    except Exception as ex:
                        print(f"can not delete rows due to {ex}")
                    return render_template("admin.html")
            else:
                return render_template('admin.html')
    return redirect(url_for('api.login'))

