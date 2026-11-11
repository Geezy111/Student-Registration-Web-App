"""
CSC 312 - Web Application Development (Tutor-Marked Assessment)
ClassMate: Flask signup application with a MySQL database.

Run:  python app.py   ->   http://127.0.0.1:5000
"""
import os
import re

import bcrypt
import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for

# 1. Setup: create the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "classmate-dev-key")

# MySQL connection details (edit here or set environment variables)
DB = dict(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DB", "classmate_db"),
)


# 3. Validation: return a list of problems (an empty list means the form is fine)
def validate_signup(username, password, confirm):
    problems = []
    if not re.fullmatch(r"[A-Za-z0-9_]{3,25}", username):
        problems.append("Username must be 3-25 characters: letters, numbers or _ only.")
    if len(password) < 8:
        problems.append("Password must have at least 8 characters.")
    elif not any(ch.isdigit() for ch in password):
        problems.append("Password must include at least one number.")
    if password != confirm:
        problems.append("The two passwords are different.")
    return problems


# 4. Database: insert a user into tbl_user (returns False if the username is taken)
def save_user(username, password_hash):
    conn = mysql.connector.connect(**DB)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tbl_user (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()


# 2. Homepage
@app.route("/")
def index():
    return render_template("index.html")


# 3. Signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", problems=[], username="")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    problems = validate_signup(username, password, confirm)
    if problems:
        return render_template("signup.html", problems=problems, username=username)

    # 5. Password security: bcrypt hash with a random salt
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        saved = save_user(username, password_hash)
    except mysql.connector.Error as err:
        print("MySQL error:", err)
        return render_template("signup.html", username=username,
                               problems=["Database error. Please try again later."])

    if not saved:
        return render_template("signup.html", username=username,
                               problems=[f"The username '{username}' is already registered."])

    flash(f"Account created. Welcome to ClassMate, {username}!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
