""" user registration and auth functionality """
from flask import redirect, url_for, render_template, request, session


from blueprints import api
from storage.user import User
from storage import db

@api.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST" and request.form["btn"] == "login":
        try:
            # check 1 if such user exists
            usr = db.session.query(User)\
                    .filter(User.name == request.form["username"])\
                    .first()
            # check 2 if the password is correct
            if usr.verify_pwd(request.form["password"]):
                return render_template(url_for(api.quantify))
            else:
                return render_template("login.html")
        except:
            return render_template("login.html")

    return render_template("login.html")



# TODO: register
# TODO: auth -> get token
# TODO: logout -> take token away

