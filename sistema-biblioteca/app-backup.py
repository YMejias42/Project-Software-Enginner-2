from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        flash("Login exitoso")
        return redirect(url_for('dashboard'))
    else:
        flash("Credenciales incorrectas")
        return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name,email,password) VALUES (?,?,?)",
        (name, email, password)
    )
    conn.commit()
    conn.close()

    flash("Usuario registrado correctamente")
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    return "Bienvenido al sistema de biblioteca"


if __name__ == '__main__':
    app.run(debug=True)