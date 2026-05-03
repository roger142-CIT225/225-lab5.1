from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "/data/contacts.db"
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "unknown")

def init_db():
    os.makedirs("/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT)")
    conn.commit()
    conn.close()

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/style.css">
    <title>Jaden Rogers</title>
</head>
<body>
    <h1>CIT225 CI/CD Pipeline - Final Project</h1>
    <p>Jaden's semester-long DevOps pipeline: lint, build, test, scan, deploy.</p>
    <p><strong>Build: {{ build }}</strong></p>

    <hr>
    <h2>Demo Database (SQLite)</h2>
    <p>Add a contact, then delete the pod to test persistence (lab 3-9 vs 4-1).</p>

    <form method="POST" action="/add">
        Name: <input name="name" required>
        Phone: <input name="phone" required>
        <button type="submit">Add</button>
    </form>

    <ul>
        {% for c in contacts %}
            <li>{{ c[1] }} - {{ c[2] }}
                <a href="/delete/{{ c[0] }}">[delete]</a>
            </li>
        {% else %}
            <li>No contacts found.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    contacts = conn.execute("SELECT id, name, phone FROM contacts").fetchall()
    conn.close()
    return render_template_string(PAGE, contacts=contacts, build=BUILD_NUMBER)

@app.route("/add", methods=["POST"])
def add():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)",
                 (request.form["name"], request.form["phone"]))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=80)
