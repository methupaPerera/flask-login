from flask import Blueprint, render_template, redirect, url_for, session

views_bp = Blueprint("views_bp", __name__)

@views_bp.route("/")
@views_bp.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("auth_bp.log_in"))
    
    user = session["user"] # Gets the user name from the session.
    return render_template("home.html", user=user)

@views_bp.route("/about")
def about():
    return render_template("about.html")