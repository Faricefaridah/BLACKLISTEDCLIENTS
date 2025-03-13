from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for session security

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('blacklist.db')
        print("Connection successful.")
    except Error as e:
        print(e)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Set your admin credentials here
        if username == 'faridah' and password == 'faridah1234':  # Updated credentials
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_client():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    id_number = request.form['id_number']
    shop = request.form['shop']
    phone_number = request.form['phone_number']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO blacklisted_clients (name, id_number, shop, phone_number) VALUES (?, ?, ?, ?)", (name, id_number, shop, phone_number))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete_client(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blacklisted_clients WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_clients():
    search_term = request.form['search_term']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blacklisted_clients WHERE name LIKE ? OR id_number LIKE ?", ('%'+search_term+'%', '%'+search_term+'%'))
    clients = cursor.fetchall()
    return render_template('index.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
