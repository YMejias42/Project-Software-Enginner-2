from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

DATABASE = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Iniciar sesión")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ───────────────────────────────────────────────────────────────
# AUTH
# ───────────────────────────────────────────────────────────────

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            flash("Dashboard")
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales incorrectas")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()

        if existing:
            conn.close()
            flash("Ya existe una cuenta con ese correo.")
            return redirect(url_for('register'))

        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?,?,?)",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        flash("Registro exitoso")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for('login'))


# ───────────────────────────────────────────────────────────────
# DASHBOARD
# ───────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    total_books     = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    available_books = conn.execute("SELECT COUNT(*) FROM books WHERE available=1").fetchone()[0]
    borrowed_books  = conn.execute("SELECT COUNT(*) FROM books WHERE available=0").fetchone()[0]
    my_loans        = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE user_id=? AND returned=0",
        (session['user_id'],)
    ).fetchone()[0]
    conn.close()

    return render_template('dashboard.html',
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books,
        my_loans=my_loans,
    )


# ───────────────────────────────────────────────────────────────
# BOOKS
# ───────────────────────────────────────────────────────────────

@app.route('/books')
@login_required
def books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('books.html', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title        = request.form['title']
        author       = request.form['author']
        cover_color  = request.form['cover_color']
        available    = 1

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO books (title, author, cover_color, available) VALUES (?,?,?,?)",
            (title, author, cover_color, available)
        )
        conn.commit()
        conn.close()

        flash("Libro añadido correctamente.")
        return redirect(url_for('books'))

    return render_template('add_book.html')


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    conn = get_db_connection()

    if request.method == 'POST':
        title       = request.form['title']
        author      = request.form['author']
        cover_color = request.form['cover_color']

        conn.execute(
            "UPDATE books SET title=?, author=?, cover_color=? WHERE id=?",
            (title, author, cover_color, book_id)
        )
        conn.commit()
        conn.close()

        flash("Libro actualizado")
        return redirect(url_for('books'))

    book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    conn.close()

    if not book:
        flash("Libro no encontrado.")
        return redirect(url_for('books'))

    return render_template('edit_book.html', book=book)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    flash("Libro eliminado")
    return redirect(url_for('books'))


# ───────────────────────────────────────────────────────────────
# LOANS
# ───────────────────────────────────────────────────────────────

@app.route('/loan/<int:book_id>', methods=['POST'])
@login_required
def loan(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()

    if not book:
        flash("No disponible")
    elif not book['available']:
        flash("No disponible")
    else:
        conn.execute(
            "INSERT INTO loans (user_id, book_id) VALUES (?,?)",
            (session['user_id'], book_id)
        )
        conn.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
        conn.commit()
        flash("Prestamo realizado")

    conn.close()
    return redirect(url_for('books'))


@app.route('/return/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    conn = get_db_connection()
    loan = conn.execute(
        "SELECT loans.*, books.title FROM loans JOIN books ON loans.book_id=books.id WHERE loans.id=? AND loans.user_id=?",
        (loan_id, session['user_id'])
    ).fetchone()

    if not loan:
        flash("Préstamo no encontrado.")
    elif loan['returned']:
        flash("Este libro ya fue devuelto.")
    else:
        conn.execute(
            "UPDATE loans SET returned=1, return_date=datetime('now') WHERE id=?",
            (loan_id,)
        )
        conn.execute("UPDATE books SET available=1 WHERE id=?", (loan['book_id'],))
        conn.commit()
        flash("Libro devuelto")

    conn.close()
    return redirect(url_for('my_loans'))


@app.route('/my_loans')
@login_required
def my_loans():
    conn  = get_db_connection()
    loans = conn.execute(
        """SELECT loans.id, books.title, books.author, books.cover_color,
                  loans.loan_date, loans.return_date, loans.returned
           FROM loans JOIN books ON loans.book_id=books.id
           WHERE loans.user_id=?
           ORDER BY loans.returned ASC, loans.loan_date DESC""",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('my_loans.html', loans=loans)


@app.route('/occupied')
@login_required
def occupied():
    conn  = get_db_connection()
    loans = conn.execute(
        """SELECT books.title, books.author, books.cover_color,
                  users.name AS borrower, loans.loan_date
           FROM loans
           JOIN books ON loans.book_id=books.id
           JOIN users ON loans.user_id=users.id
           WHERE loans.returned=0
           ORDER BY loans.loan_date DESC"""
    ).fetchall()
    conn.close()
    return render_template('occupied.html', loans=loans)


# ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
