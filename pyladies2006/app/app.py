""" factory method for app creation: 
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html """
from flask import Flask 
from storage import db
import os


def app_factory(environment: str) -> Flask:
    """ Step by step creation and customization of a flask app """ 

    # app instance
    app = Flask("self-quantify-app-pyladies")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'postgresql://localhost:5432/quantify')
    app.config['SECRET_KEY'] = os.environ.get('SECRET', 'sdohsd&sa!')
    
    # blueprints a.k.a. functionality
    from blueprints import api
    app.register_blueprint(api)

    # database connection and preparation
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


environment = os.environ.get('DEPLOYMENT', 'local')
app = app_factory(environment)
