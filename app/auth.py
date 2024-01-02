from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import db
from .models import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    # Redirects the user to home if logged in.
    if "user" in session:
        flash("Please logout before login into another account.", "warning")
        return redirect(url_for("views_bp.home"))
    
    # Handles the signup.
    if request.method == "POST":
        # Gets all the information from the form and removes the extra spaces.
        full_name = request.form.get("full_name").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("confirm_password").strip()

        # Validating the form values.
        state = validate_signup(full_name, email, password, confirm_password)
        
        # Id values are validated, the user will be redirected to home, sign up otherwise.
        if state:
            found_user = User.query.filter_by(email=email).first()

            if found_user:
                flash("The email you entered is already exists.", "danger")
                flash("Failed to create the account.", "danger")
                return render_template("auth/sign-up.html")
            else:
                new_user = User(full_name, email, password)
                db.session.add(new_user)
                db.session.commit()

                session.permanent = True
                session["user"] = full_name

                flash("Your account has been created successfully.", "success")
                return redirect(url_for("views_bp.home"))

        else:
            return render_template("auth/sign-up.html")
    
    return render_template("auth/sign-up.html")


@auth_bp.route("/log-in", methods=["GET", "POST"])
def log_in():
    # Redirects the user to home if logged in.
    if "user" in session:
        flash("Please logout before login into another account.", "warning")
        return redirect(url_for("views_bp.home"))
    
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        found_user = User.query.filter_by(email=email).first()

        if found_user:
            if found_user.password != password:
                flash("Incorrect password.", "danger")
                return render_template("auth/log-in.html")
            else:
                session.permanent = True
                session["user"] = found_user.full_name

                flash("Login success.", "success")
                return redirect(url_for("views_bp.home"))
        else:
            flash("Email not found. Sign up instead.", "danger")
            return render_template("auth/log-in.html")


    return render_template("auth/log-in.html")

@auth_bp.route("/log-out", methods=["GET", "POST"])
def log_out():
    if "user" in session:
        user = session["user"]
        session.pop("user")
        flash(f"You have been logged out {user}.", "success")
    else:
        flash("Please log in.", "warning")
        
    return redirect(url_for("auth_bp.log_in"))
        
# Utilities #############################################

def validate_signup(full_name, email, password, confirm_password) -> bool:
    """
    @params: full_name, email, password, confirm_password
    @returns: True if successful, False otherwise
    """

    state = True

    if len(full_name) < 2 or len(email) < 11:
        flash("Please provide valid information.", "danger")
        state = False

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        state = False

    if password != confirm_password or password == "" or confirm_password == "":
        flash("Please check your passwords.", "danger")
        state = False

    return state

