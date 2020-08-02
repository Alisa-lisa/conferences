""" user registration and auth functionality """
from flask import redirect, url_for, render_template, request, session
import logging

from blueprints import api
from storage.user import User
from storage import db
import os

logger = logging.getLogger(__name__)


@api.route("/", methods=["POST", "GET"])
def login():
    """ Attempt to login for exising user """
    if 'users' not in session:
        session['users'] = []
    if request.method == "POST": 
        if request.form["btn"] == "login":
            try:
                # check 1 if such user exists
                usr = db.session.query(User)\
                        .filter(User.username == request.form["login"])\
                        .first()
                # check 2 if the password is correct
                if usr.verify_pwd(request.form["password"]):
                    token = usr.current_auth_token
                    # check for token 
                    if token is None:
                        token = usr.generate_auth_token
                    session['users'].append(usr.current_auth_token)
                    return redirect(url_for("api.quantify"))
                else:
                    return render_template("login.html")
            except Exception as ex:
                logger.error(f"could not log in the user {request.form['login']} due to {ex}")
                return render_template("login.html")
        else:
            new_user = User(str(request.form["login"]), str(request.form["password"]))
            try:
                # let SQL handle duplicate dtection on username
                db.session.add(new_user)
                db.session.commit()
                return render_template("login.html")
            except Exception as ex:
                print(f"could not add a new user {new_user.__repr__} due to {ex}")
                return render_template("login.html")

    return render_template("login.html")



@api.route("/logout")
def logout():
    """ terminate session """
    pass

