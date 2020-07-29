""" factory method for app creation: 
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html """
from flask import Flask


def app_factory(environment: str) -> Flask:
    """ Step by step creation and customization of a flask app """ 

    # app instance
    app = Flask("self-quantify-app-pyladies")


    # blueprints a.k.a. functionality
    from .blueprints import api
    app.register_blueprint(api)

    # database connection and preparation
    

    return app




