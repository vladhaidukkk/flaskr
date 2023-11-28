from flask import Blueprint, render_template

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
