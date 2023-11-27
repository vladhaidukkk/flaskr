import functools

from flask import Blueprint, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

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


@bp.route("/login", methods=("GET", "POST"))
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if not error:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

    return render_template("auth/login.jinja", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )
    else:
        g.user = None


def login_required(view):
    @functools.wraps(view)
    def view_wrapper(**kwargs):
        if not g.user:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return view_wrapper
