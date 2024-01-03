import re
from flask import flash
from .models import User

def validate_signup(full_name, email, password, confirm_password) -> bool:
    """
    Requirements:
        Users full name
        Email
        Password
        Password confirmation

    Task:
        Validating the sign up details.
    
    Returns:
        Validation status
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
    
    if User.query.filter_by(email=email).first():
        flash("User already exists.", "danger")
        state = False

    if not check_password_strength(password):
        flash("Please enter a strong password mixed with numbers, letters and symbols.", "danger")
        state = False

    if not validate_email(email):
        flash("Emails should not contain characters other than @ . letters and numbers.", "danger")
        state = False

    if not validate_name(full_name):
        flash("Names should not contain characters other than letter.", "danger")
        state = False

    return state

def check_password_strength(password):
    # Define regular expressions for numbers, characters, and symbols
    contains_number = bool(re.search(r"\d", password))  # Check for at least one digit
    contains_char = bool(re.search(r"[a-zA-Z]", password))  # Check for at least one character
    contains_symbol = bool(re.search(r"[\W_]", password))  # Check for at least one symbol

    # Check if all criteria are met.
    if contains_number and contains_char and contains_symbol:
        return True
    else:
        return False
    
def validate_email(email):
    # Define the regular expression pattern for a valid email.
    pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # Check if the email matches the pattern.
    if re.match(pattern, email):
        return True  # Email is valid.
    else:
        return False  # Email is not valid.

def validate_name(input_string):
    # Define the regular expression pattern for letters only.
    pattern = r"^[a-zA-Z]+$"

    # Check if the input string matches the pattern.
    if re.match(pattern, input_string):
        return True  # Input contains only letters.
    else:
        return False  # Input contains characters other than letters.
