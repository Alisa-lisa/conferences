from storage import db
from storage.user import User


class Quantify(db.Model):
    __tablename__ = "worklife"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    usr_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    activity = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)  # mastery/fun/chores
    stress = db.Column(db.Integer, nullable=True)  # on the scale 1 to 10 how stressed are you
    happiness = db.Column(db.Integer, nullable=True) # on the scale 1 to 10 how happy are you

    def to_list(self):
        """ representation of one object in a list format for easier csv write """
        return [self.timestamp, self.activity, self.category, self.stress, self.happiness]
