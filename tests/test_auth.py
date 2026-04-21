def test_register_user_success(client):
    response = client.post("/register", data={
        "name": "testuser",
        "email": "test@example.com",
        "password": "1234"
    }, follow_redirects=True)

    assert b"Registro exitoso" in response.data


def test_login_valid_credentials(client):
    # Registrar usuario primero
    client.post("/register", data={
        "name": "user",
        "email": "user@example.com",
        "password": "pass"
    })

    # Intentar login
    response = client.post("/login", data={
        "email": "user@example.com",
        "password": "pass"
    }, follow_redirects=True)

    assert b"Dashboard" in response.data


def test_login_invalid_credentials(client):
    response = client.post("/login", data={
        "email": "wrong@example.com",
        "password": "incorrect"
    }, follow_redirects=True)

    assert b"Credenciales incorrectas" in response.data
