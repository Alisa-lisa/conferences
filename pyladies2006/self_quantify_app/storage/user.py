""" User and tokens DAO """
from self_quantify_app.storage import db
from self_quantify_app.helpers import hasher
import uuid
import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True)
    pwhash = db.Column(db.String, unique=True)
    current_auth_token = db.Column(db.String(120), index=True)
    last_action = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.pwhash = self.set_pwd(password)

    def __repr__(self):
        return f"User: self.username"

    def set_pwd(self, password):
        return hasher.hash(f"{self.username}{password}")

    def verify_pwd(self, password):
        return hasher.hash(f"{self.username}{password}", self.pwhash)

    def generate_auth_token(self):
        """Generate an auth token and save it to the `current_auth_token` column."""
        self.current_auth_token = str(uuid.uuid4)
        self.last_action = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self.current_auth_token 

