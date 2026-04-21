def test_loan_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    client.post("/add_book", data={"title": "A", "author": "B", "year": "2020"})
    response = client.get("/loan/1", follow_redirects=True)
    assert b"Prestamo realizado" in response.data

def test_return_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    client.post("/add_book", data={"title": "A", "author": "B", "year": "2020"})
    client.get("/loan/1")
    response = client.get("/return/1", follow_redirects=True)
    assert b"Libro devuelto" in response.data

def test_cannot_loan_occupied_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    client.post("/add_book", data={"title": "A", "author": "B", "year": "2020"})
    client.get("/loan/1")
    response = client.get("/loan/1", follow_redirects=True)
    assert b"No disponible" in response.data
