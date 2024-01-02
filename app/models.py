from . import db
from sqlalchemy.sql import func

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.password = password