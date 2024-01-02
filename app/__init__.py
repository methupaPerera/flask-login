from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ube tatta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.permanent_session_lifetime = timedelta(hours=1)
    db.init_app(app)

    from .views import views_bp
    from .auth import auth_bp

    app.register_blueprint(views_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/")
    
    with app.app_context():
        db.drop_all()
        db.create_all()

    return app
