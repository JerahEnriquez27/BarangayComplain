from flask import Flask, render_template, request
from Database import get_connection

app = Flask(__name__)

@app.route('/main')
def main():
    return render_template('Main.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/register')
def register():
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
