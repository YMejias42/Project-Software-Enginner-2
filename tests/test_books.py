def test_add_book(client):
    # Login correcto
    client.post("/login", data={
        "email": "admin@biblioteca.com",
        "password": "admin123"
    })

    # Añadir libro
    response = client.post("/add_book", data={
        "title": "Libro Test",
        "author": "Autor",
        "cover_color": "#FFFFFF"
    }, follow_redirects=True)

    assert b"Libro a" in response.data  # "Libro añadido correctamente."


def test_edit_book(client):
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

    # Editar libro
    response = client.post("/edit_book/1", data={
        "title": "Nuevo",
        "author": "Autor",
        "cover_color": "#123456"
    }, follow_redirects=True)

    assert b"actualizado" in response.data.lower()  # "Libro actualizado"


def test_delete_book(client):
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

    # Eliminar libro (POST, no GET)
    response = client.post("/delete_book/1", follow_redirects=True)

    assert b"eliminado" in response.data.lower()  # "Libro eliminado"
