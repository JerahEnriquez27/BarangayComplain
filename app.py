from flask import Flask, render_template, request, redirect, url_for, session
from Database import get_connection

app = Flask(__name__)
app.secret_key = 'secretnijerah'

@app.route('/main')
def main():
    return render_template('Main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password."
            return render_template('Login.html', error=error)

    return render_template('Login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        address = request.form['address']
        contact = request.form['contact']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists!"
        else:
            cursor.execute("""
                INSERT INTO users (fullname, username, address, contact, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (fullname, username, address, contact, password))
            conn.commit()
            cursor.close()
            conn.close()
            return "Registration successful!"
    return render_template('Register.html')


@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/profile')
def profile():
    return render_template('Profile.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/editprofile')
def editprofile():
    return render_template('EditProfile.html')

if __name__ == '__main__':
    app.run(debug=True)
