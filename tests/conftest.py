import sys
import os

# Agregar la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app
from init_db import init_db
import tempfile


@pytest.fixture
def client():
    db_fd, temp_db = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["DATABASE"] = temp_db

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(temp_db)
