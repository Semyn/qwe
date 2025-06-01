from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            age INTEGER,
            registration_date TEXT DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return 'Некорректный email', 400
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            return 'Некорректный возраст', 400
    except ValueError:
        return 'Возраст должен быть числом', 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, age, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (name, email, age_int, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return 'Email уже зарегистрирован', 400
    conn.close()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return 'Данные успешно сохранены!'

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users_list = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)