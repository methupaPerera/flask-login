from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .utils import validate_signup

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
            # Checks if a user is already logged with the email.
            found_user = User.query.filter_by(email=email).first()

            # Creates a new user account if the email is new.
            if found_user:
                flash("The email you entered is already exists.", "danger")
                flash("Failed to create the account.", "danger")

                return render_template("auth/sign-up.html")
            else:
                new_user = User(full_name, email)
                new_user.set_password(password)

                db.session.add(new_user)
                db.session.commit()

                # Adding the user name to the session.
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
    
    # Handles the login.
    if request.method == "POST":
        # Gets all the information from the form and removes the extra spaces.
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        # Checks if a user exists with the email entered.
        found_user = User.query.filter_by(email=email).first()

        # Checks for the password if the user exists.
        if found_user:
            if not found_user.check_password(password):
                flash("Incorrect password.", "danger")
                return render_template("auth/log-in.html")
            else:
                # Adding user name to the session.
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
    # Removes the user from the session.
    if "user" in session:
        user = session["user"]
        session.pop("user")
        flash(f"You have been logged out {user}.", "success")
    else:
        flash("Please log in.", "warning")
        
    return redirect(url_for("auth_bp.log_in"))

