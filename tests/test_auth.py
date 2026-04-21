def test_register_user_success(client):
    response = client.post("/register", data={
        "username": "testuser",
        "password": "1234"
    }, follow_redirects=True)
    assert b"Registro exitoso" in response.data

def test_login_valid_credentials(client):
    client.post("/register", data={"username": "user", "password": "pass"})
    response = client.post("/login", data={
        "username": "user",
        "password": "pass"
    }, follow_redirects=True)
    assert b"Dashboard" in response.data

def test_login_invalid_credentials(client):
    response = client.post("/login", data={
        "username": "wrong",
        "password": "incorrect"
    })
    assert b"Credenciales incorrectas" in response.data
