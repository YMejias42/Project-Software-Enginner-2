def test_dashboard_loads(client):
    # Login correcto usando el usuario creado en init_db.py
    client.post("/login", data={
        "email": "admin@biblioteca.com",
        "password": "admin123"
    })

    # Acceder al dashboard
    response = client.get("/dashboard")

    # Debe cargar correctamente
    assert response.status_code == 200
    assert b"Dashboard" in response.data
