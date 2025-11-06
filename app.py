from flask import Flask, render_template, request, redirect, url_for, session
from Database import get_connection

app = Flask(__name__)
app.secret_key = 'secretnijerah'

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/complaintboard')
def complaintboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id, c.category AS title, c.text_description AS description,
               c.location, c.complain_status AS status, c.date_filed AS date,
               u.fullname AS filed_by FROM complaints c JOIN users u ON c.user_id = u.id ORDER BY c.date_filed DESC
    """)
    complaints = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('complaintboard.html', complaints=complaints)

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
        email = request.form['email']
        address = request.form['address']
        contact = request.form['contact']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match!"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return "Username or email already exists!"

        cursor.execute("""
            INSERT INTO users (fullname, username, email, address, contact, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fullname, username, email, address, contact, password))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('Register.html')


@app.route('/complain', methods=['GET', 'POST'])
def complain():
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        location = request.form['location']
        
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('login'))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO complaints (user_id, category, text_description, location, complain_status, date_filed)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, category, description, location, "Pending"))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('complaintboard'))

    return render_template('Complain.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT fullname, username, email, address, contact FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('Profile.html', user=user)

@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        address = request.form['address']
        contact = request.form['contact']

        cursor.execute("""
            UPDATE users 
            SET fullname = %s, username = %s, email = %s, address = %s, contact = %s
            WHERE id = %s
        """, (fullname, username, email, address, contact, user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('profile'))
    else:
        cursor.execute("SELECT fullname, username, email, address, contact FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('EditProfile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
