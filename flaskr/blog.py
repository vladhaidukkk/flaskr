from flask import Blueprint, g, redirect, render_template, request, url_for

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created_at, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created_at DESC"
    ).fetchall()
    return render_template("blog/index.jinja", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    error = None

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        if not title:
            error = "Title is required."
        elif not body:
            error = "Body is required."

        if not error:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.jinja", error=error)
