""" user registration and auth functionality """
from flask import redirect, url_for, render_template, request, session
import logging

from self_quantify_app.blueprints import api
from self_quantify_app.storage.user import User
from self_quantify_app.storage import db


logger = logging.getLogger(__name__)


@api.route("/", methods=["POST", "GET"])
def login():
    """ Attempt to login for exising user """
    if request.method == "POST" and request.form["btn"] == "login":
        try:
            # check 1 if such user exists
            usr = db.session.query(User)\
                    .filter(User.name == request.form["username"])\
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
            logger.error(f"could not log in the user {usr.__repr__} due to {ex}")
            return render_template("login.html")

    return render_template("login.html")


@api.route("/register", methods=["POST", "GET"])
def register():
    """ Add new user to DB. No restrictions on number of users """
    if request.method == "POST" and request.form["btn"] == "register":
        try:
            # let SQL handle duplicate dtection on username
            new_user = User(request.form["username"], request.form["password"])
            db.session.add(new_user)
            db.session.commit()
            
        except Exception as ex:
            logger.error(f"could not add a new user {new_user.__repr__} due to {ex}")

        return redirect(url_for("api.login"))
    return render_template("login.html")


@api.route("/logout")
def logout():
    """ terminate session """
    pass
# TODO: logout -> take token away

