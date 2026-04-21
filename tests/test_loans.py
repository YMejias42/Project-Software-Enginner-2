def test_loan_book(client):
    # Login correcto
    client.post("/login", data={
        "email": "admin@biblioteca.com",
        "password": "admin123"
    })

    # Crear libro
    client.post("/add_book", data={
        "title": "A",
        "author": "B",
        "cover_color": "#000000"
    })

    # Prestar libro (POST, no GET)
    response = client.post("/loan/1", follow_redirects=True)

    assert b"prestamo realizado" in response.data.lower()


def test_return_book(client):
    # Login correcto
    client.post("/login", data={
        "email": "admin@biblioteca.com",
        "password": "admin123"
    })

    # Crear libro
    client.post("/add_book", data={
        "title": "A",
        "author": "B",
        "cover_color": "#000000"
    })

    # Prestar libro
    client.post("/loan/1")

    # Devolver libro (POST, no GET)
    response = client.post("/return/1", follow_redirects=True)

    assert b"libro devuelto" in response.data.lower()


def test_cannot_loan_occupied_book(client):
    # Login correcto
    client.post("/login", data={
        "email": "admin@biblioteca.com",
        "password": "admin123"
    })

    # Crear libro
    client.post("/add_book", data={
        "title": "A",
        "author": "B",
        "cover_color": "#000000"
    })

    # Primer préstamo
    client.post("/loan/1")

    # Intentar prestar de nuevo
    response = client.post("/loan/1", follow_redirects=True)

    assert b"no disponible" in response.data.lower()
