import sys
import os
import pytest
import tempfile

# Agregar la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from init_db import init_db


@pytest.fixture
def client():
    # Crear base de datos temporal
    db_fd, temp_db = tempfile.mkstemp()

    # Crear la app en modo testing
    app = create_app({
        "TESTING": True,
        "DATABASE": temp_db
    })

    # Crear cliente de pruebas
    with app.test_client() as client:
        with app.app_context():
            init_db()  # Crear tablas en la BD temporal
        yield client

    # Limpiar archivo temporal
    os.close(db_fd)
    os.unlink(temp_db)
