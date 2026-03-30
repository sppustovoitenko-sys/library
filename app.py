from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "database.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            description TEXT,
            year INTEGER,
            image_url TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/library')
def library():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY id DESC")
    books = cursor.fetchall()
    conn.close()
    return render_template('library.html', books=books)

@app.route('/book/<int:id>')
def book_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (id,))
    book = cursor.fetchone()
    conn.close()
    return render_template('book_detail.html', book=book)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    year = request.form['year']
    image_url = request.form['image_url']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, description, year, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, author, description, year, image_url, datetime.now()))
    conn.commit()
    conn.close()

    return redirect(url_for('library'))

@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('library'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)