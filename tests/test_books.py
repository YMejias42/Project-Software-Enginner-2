def test_add_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    response = client.post("/add_book", data={
        "title": "Libro Test",
        "author": "Autor",
        "year": "2024"
    }, follow_redirects=True)
    assert b"Libro agregado" in response.data

def test_edit_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    client.post("/add_book", data={"title": "A", "author": "B", "year": "2020"})
    response = client.post("/edit_book/1", data={
        "title": "Nuevo",
        "author": "Autor",
        "year": "2024"
    }, follow_redirects=True)
    assert b"Actualizado" in response.data

def test_delete_book(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    client.post("/add_book", data={"title": "A", "author": "B", "year": "2020"})
    response = client.get("/delete_book/1", follow_redirects=True)
    assert b"Eliminado" in response.data
