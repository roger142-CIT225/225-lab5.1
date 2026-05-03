from flask import Flask, request, redirect, render_template_string, jsonify
import sqlite3
import os
import socket

app = Flask(__name__)
DB_PATH = "/data/contacts.db"
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "unknown")
ENV_NAME = os.environ.get("ENV_NAME", "unknown")
POD_NAME = socket.gethostname()

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
    <style>
        table { border-collapse: collapse; width: 100%; max-width: 600px; margin-top: 1em; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        th { background: #222; color: #fff; }
        .status-box { background: #f4f4f4; border: 1px solid #ccc; padding: 12px; margin-top: 1em; max-width: 600px; font-family: monospace; }
        .status-box span { color: #0a7d28; font-weight: bold; }
        form { margin-top: 1em; }
        input { padding: 6px; margin-right: 8px; }
        button { padding: 6px 14px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>CIT225 CI/CD Pipeline - Final Project</h1>
    <p>Jaden's semester-long DevOps pipeline: lint, build, test, scan, deploy.</p>
    <p><strong>Build: {{ build }}</strong> | <strong>Env: {{ env }}</strong> | <strong>Pod: {{ pod }}</strong></p>

    <hr>
    <h2>Deployment Status</h2>
    <div class="status-box" id="status">Loading...</div>

    <hr>
    <h2>Demo Database (SQLite)</h2>
    <p>Add a contact, then delete the pod to test persistence (lab 3-9 vs 4-1).</p>

    <form id="add-form">
        <input name="name" placeholder="Name" required>
        <input name="phone" placeholder="Phone" required>
        <button type="submit">Add</button>
    </form>

    <table id="contacts-table">
        <thead>
            <tr><th>ID</th><th>Name</th><th>Phone</th><th>Action</th></tr>
        </thead>
        <tbody id="contacts-body"></tbody>
    </table>

<script>
async function loadContacts() {
    const res = await fetch('/api/contacts');
    const data = await res.json();
    const body = document.getElementById('contacts-body');
    body.innerHTML = '';
    if (data.length === 0) {
        body.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">No contacts found.</td></tr>';
        return;
    }
    for (const c of data) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${c.id}</td><td>${c.name}</td><td>${c.phone}</td><td><a href="#" onclick="del(${c.id});return false;">[delete]</a></td>`;
        body.appendChild(row);
    }
}

async function del(id) {
    await fetch('/api/delete/' + id, { method: 'POST' });
    loadContacts();
}

document.getElementById('add-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    await fetch('/api/add', { method: 'POST', body: data });
    form.reset();
    loadContacts();
});

async function loadStatus() {
    const res = await fetch('/api/status');
    const data = await res.json();
    document.getElementById('status').innerHTML =
        `Build: <span>${data.build}</span><br>` +
        `Environment: <span>${data.env}</span><br>` +
        `Pod: <span>${data.pod}</span><br>` +
        `Status: <span>RUNNING</span><br>` +
        `Uptime: <span>${data.uptime}s</span>`;
}

loadContacts();
loadStatus();
setInterval(loadContacts, 3000);
setInterval(loadStatus, 5000);
</script>
</body>
</html>
"""

import time
START_TIME = time.time()

@app.route("/")
def index():
    return render_template_string(PAGE, build=BUILD_NUMBER, env=ENV_NAME, pod=POD_NAME)

@app.route("/api/contacts")
def api_contacts():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, name, phone FROM contacts").fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "phone": r[2]} for r in rows])

@app.route("/api/add", methods=["POST"])
def api_add():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)",
                 (request.form["name"], request.form["phone"]))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/delete/<int:id>", methods=["POST"])
def api_delete(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/status")
def api_status():
    return jsonify({
        "build": BUILD_NUMBER,
        "env": ENV_NAME,
        "pod": POD_NAME,
        "uptime": int(time.time() - START_TIME)
    })

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=80)
