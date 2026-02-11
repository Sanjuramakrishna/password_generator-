from flask import Flask, render_template, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# connect to database
def get_db_connection():
    conn = sqlite3.connect("passwords.db")
    return conn

# create table (runs once)
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT
)
""")
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-password")
def generate_password():
    chars = string.ascii_letters + string.digits + "@#$%&*"
    password = "".join(random.choice(chars) for _ in range(8))

    conn = get_db_connection()
    conn.execute("INSERT INTO passwords (password) VALUES (?)", (password,))
    conn.commit()
    conn.close()

    return jsonify({"password": password})

if __name__ == "__main__":
    app.run(debug=True)
