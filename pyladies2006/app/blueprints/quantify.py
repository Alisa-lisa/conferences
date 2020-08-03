from flask import redirect, url_for, render_template, request, session
import logging

from blueprints import api
from storage.quantify import Quantify
from storage.user import User
from storage import db
import datetime

logger = logging.getLogger(__name__)


@api.route("/quantify", methods=["POST", "GET"])
def quantify():
    """ Save tracking info for work-life-chores- balance form """
    # only logged in user can see this
    if 'user' in session: 
        usr = db.session.query(User)\
                .filter(User.current_auth_token == session['user'])\
                .first()
        # now we associate the form with our active user
        if request.method == "POST":
            print(request.form)
            try:
                record = Quantify(usr_id=usr.id, 
                        timestamp=datetime.datetime.now(),
                        activity=request.form['activity'],
                        category=request.form['category'],
                        stress=request.form['stress'],
                        happiness=request.form['happiness'])
                db.session.add(record)
                db.session.commit()
            except Exception as ex:
                logger.error(f"Can not write record due to {ex}")
                db.session.rollback()
            return render_template('actions_form.html')
        return render_template('actions_form.html')
    else:
        return redirect(url_for('api.login'))
