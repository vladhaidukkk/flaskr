from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if not error:
            db = get_db()

            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

    return render_template("auth/register.jinja", error=error)


@bp.route("/login")
def login():
    return render_template("auth/login.jinja")
