from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from uuid import uuid4

db = SQLAlchemy() # Creating SQLAlchemy instance.
DB_NAME = "users.sqlite3" # Database name.
SECRET_KEY = uuid4().hex # Secret key generated with uuid for authentication.

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    # Setting session expiration time.
    app.permanent_session_lifetime = timedelta(hours=1)

    # Initializing database with flask instance.
    db.init_app(app)

    # Importing all flask views.
    from .views import views_bp
    from .auth import auth_bp

    # Registering all views.
    app.register_blueprint(views_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/")
    
    # Creating database.
    with app.app_context():
       db.create_all()

    return app # Returning the created flask app instance.
