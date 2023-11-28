from flask import Blueprint, abort, g, redirect, render_template, request, url_for

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


def get_post(post_id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created_at, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (post_id,),
        )
        .fetchone()
    )

    if not post:
        abort(404, f"Post {post_id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    post = get_post(id)
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
                "UPDATE post SET title = ?, body = ? WHERE id = ?",
                (title, body, id),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.jinja", post=post, error=error)
