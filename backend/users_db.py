
from flask_sqlalchemy import SQLAlchemy

from backend import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return "User({}, {})".format(self.name, self.password)


