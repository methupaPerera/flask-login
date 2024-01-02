from flask import Blueprint, render_template, redirect, url_for, session
from . import db
from .models import User

views_bp = Blueprint("views_bp", __name__)

@views_bp.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("auth_bp.log_in"))
    
    user = session["user"]
    return render_template("home.html", user=user)
        
