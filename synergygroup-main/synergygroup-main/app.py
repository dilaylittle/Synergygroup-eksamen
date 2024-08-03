from flask import Flask, render_template, request, redirect, url_for, session, flash
from get_menu_data import scrape_menu
from db import get_db_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html', admin_logged_in=session.get('admin_logged_in'))

@app.route('/about')
def about():
    return render_template('about.html', admin_logged_in=session.get('admin_logged_in'))

@app.route('/services')
def services():
    return render_template('services.html', admin_logged_in=session.get('admin_logged_in'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
            connection.commit()
            cursor.close()
            connection.close()
            return render_template('thank_you.html', admin_logged_in=session.get('admin_logged_in'))
        else:
            return "Failed to connect to the database"
    return render_template('contact.html', admin_logged_in=session.get('admin_logged_in'))

@app.route('/menu')
def menu():
    week_number, menus = scrape_menu()
    return render_template('menu.html', menus=menus, week_number=week_number, admin_logged_in=session.get('admin_logged_in'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', admin_logged_in=session.get('admin_logged_in'))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name, email, message FROM contacts")
        contacts = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('admin.html', contacts=contacts, admin_logged_in=True)
    else:
        return "Failed to connect to the database"

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
