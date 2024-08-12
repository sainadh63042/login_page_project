from flask import Flask, request, render_template, url_for, redirect
import mysql.connector

app = Flask(__name__)

#mysql database connection
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'sainadh123',
    database = 'sainadh'
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INT AUTO_INCREMENT PRIMARY KEY,
               user_name VARCHAR(255) NOT NULL,
               first_name VARCHAR(255) NOT NULL,
               last_name VARCHAR(255) NOT NULL,
               password VARCHAR(255) NOT NUll
               )
""")
@app.route('/login_page', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pword']

        cursor.execute("SELECT * FROM users WHERE user_name = %s AND password = %s", (uname, pword))
        user_credentials = cursor.fetchone()
        if user_credentials:
            return "Login successful."
        else:
            return "Invalid credentials."
    return render_template("login_page.html")
@app.route('/register_page', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        fname = request.form['fname']
        lname = request.form['lname']
        spword = request.form['spword']
        cpword = request.form['cpword']

        # Simple validation: Check if passwords match
        if spword != cpword:
            return "Passwords do not match!", 400

        # Store user data into the database
        cursor.execute("INSERT INTO users (user_name, first_name, last_name, password) VALUES (%s, %s, %s, %s)", (uname, fname, lname, spword))
        db.commit()

        return "Registration successful!"
    return render_template("register_page.html")

if __name__ == '__main__':
    app.run(debug=True)
