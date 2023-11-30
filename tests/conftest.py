import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rt") as f:
        db_sql = f.read()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )
    with app.app_context():
        init_db()
        get_db().executescript(db_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()