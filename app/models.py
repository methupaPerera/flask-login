from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(255))

    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email

    # Hash the password.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks the passwords when a user logs in.
    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
