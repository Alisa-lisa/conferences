""" User and tokens DAO """
from .storage import db
from .helpers import passlib


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=True)
    pwhash = db.Column(String, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.pwhash = self.set_pwd(password)

    def set_pwd(self, password):
        return passlib.hash(f"{self.username}{password}")

    def verify_pwd(self, password):
        return passlib.hash(f"{self.username}{password}", self.pwhash)

    
