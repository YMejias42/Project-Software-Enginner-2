"""
init_db.py — Inicializa la base de datos SQLite usando la configuración de la app.
"""

import sqlite3
from flask import current_app


def init_db():
    # Usar la base de datos definida en la app (producción o testing)
    database = current_app.config["DATABASE"]

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # ── Tabla: usuarios ──────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL
        )
    """)

    # ── Tabla: libros ────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            author      TEXT    NOT NULL,
            genre       TEXT,
            year        INTEGER,
            cover_color TEXT    DEFAULT '#3D5A47',
            available   INTEGER DEFAULT 1,
            UNIQUE(title, author)   -- Evita duplicados reales
        )
    """)

    # ── Tabla: préstamos ─────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            book_id     INTEGER NOT NULL REFERENCES books(id),
            loan_date   TEXT    DEFAULT (datetime('now')),
            return_date TEXT,
            returned    INTEGER DEFAULT 0
        )
    """)

    # ── Insertar datos de ejemplo solo si no hay libros ──────────────────────
    cur.execute("SELECT COUNT(*) FROM books")
    book_count = cur.fetchone()[0]

    if book_count == 0:
        sample_books = [
            ("Cien años de soledad",    "Gabriel García Márquez", "Novela",    1967, "#C4714F"),
            ("El Quijote",              "Miguel de Cervantes",    "Clásico",   1605, "#3D5A47"),
            ("1984",                    "George Orwell",          "Distopía",  1949, "#0D0D0D"),
            ("El principito",           "Antoine de Saint-Exupéry","Fábula",   1943, "#B8A84A"),
            ("Rayuela",                 "Julio Cortázar",         "Novela",    1963, "#5A3D6E"),
            ("Ficciones",               "Jorge Luis Borges",      "Cuentos",   1944, "#2C5F7A"),
            ("La sombra del viento",    "Carlos Ruiz Zafón",      "Misterio",  2001, "#8B4513"),
            ("Beloved",                 "Toni Morrison",          "Novela",    1987, "#4A7C59"),
            ("Don Quijote de la Mancha","Miguel de Cervantes",    "Clásico",   1615, "#6B4E3D"),
            ("Pedro Páramo",            "Juan Rulfo",             "Novela",    1955, "#7A5C3D"),
        ]

        cur.executemany(
            "INSERT INTO books (title, author, genre, year, cover_color) VALUES (?,?,?,?,?)",
            sample_books
        )

    # ── Usuario de prueba ────────────────────────────────────────────────────
    cur.execute(
        "INSERT OR IGNORE INTO users (name, email, password) VALUES (?,?,?)",
        ("Admin", "admin@biblioteca.com", "admin123")
    )

    conn.commit()
    conn.close()