def test_dashboard_loads(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.data
