def test_protected_routes_require_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert "Iniciar sesión".encode() in response.data

def test_static_files_load(client):
    response = client.get("/static/style.css")
    assert response.status_code == 200
