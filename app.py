from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os
import socket
import time

app = Flask(__name__)
DB_PATH = "/data/contacts.db"
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "unknown")
ENV_NAME = os.environ.get("ENV_NAME", "unknown")
POD_NAME = socket.gethostname()
START_TIME = time.time()

def init_db():
    os.makedirs("/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT)")
    conn.commit()
    conn.close()

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaden Rogers — CI/CD Final</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --bg: #0a0a0f;
            --bg-card: #14141c;
            --bg-elevated: #1c1c26;
            --border: #2a2a36;
            --border-hover: #3a3a48;
            --text: #f4f4f7;
            --text-muted: #8b8b96;
            --accent: #7c5cff;
            --accent-glow: rgba(124, 92, 255, 0.15);
            --success: #4ade80;
            --danger: #f87171;
            --warning: #fbbf24;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            background-image:
                radial-gradient(at 20% 0%, var(--accent-glow) 0px, transparent 50%),
                radial-gradient(at 80% 100%, rgba(74, 222, 128, 0.08) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text);
            min-height: 100vh;
            padding: 40px 20px;
            line-height: 1.6;
        }

        .container { max-width: 900px; margin: 0 auto; }

        .header { margin-bottom: 32px; }
        .header h1 {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #fff 0%, #a8a8b8 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .header p { color: var(--text-muted); font-size: 15px; }

        .badges { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 16px; }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 999px;
            font-size: 13px;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
        }
        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }
        .badge strong { color: var(--text); font-weight: 500; }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }

        .card h2 {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 16px;
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
        }
        .status-item {
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 14px;
        }
        .status-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .status-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: var(--text);
            word-break: break-all;
        }
        .status-value.live {
            color: var(--success);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        form { display: flex; gap: 8px; flex-wrap: wrap; }
        input[type=text], input:not([type]) {
            flex: 1;
            min-width: 180px;
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text);
            font-family: inherit;
            font-size: 14px;
            transition: border-color 0.15s, box-shadow 0.15s;
        }
        input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        input::placeholder { color: var(--text-muted); }

        button {
            background: var(--accent);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-family: inherit;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: transform 0.05s, background 0.15s;
        }
        button:hover { background: #6a4ce8; }
        button:active { transform: scale(0.98); }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4px;
        }
        thead tr { border-bottom: 1px solid var(--border); }
        th {
            text-align: left;
            padding: 10px 12px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            font-weight: 600;
        }
        td {
            padding: 14px 12px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
            color: var(--text);
        }
        tbody tr:hover { background: var(--bg-elevated); }
        tbody tr:last-child td { border-bottom: none; }

        .id-cell {
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            font-size: 13px;
        }

        .delete-btn {
            background: transparent;
            color: var(--danger);
            border: 1px solid transparent;
            padding: 4px 10px;
            font-size: 12px;
            border-radius: 6px;
        }
        .delete-btn:hover {
            background: rgba(248, 113, 113, 0.1);
            border-color: var(--danger);
        }

        .empty {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
            font-size: 14px;
        }

        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 32px;
            font-family: 'JetBrains Mono', monospace;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .pulse { animation: pulse 2s infinite; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CIT225 CI/CD Pipeline</h1>
            <p>Semester-long DevOps pipeline · lint · build · test · scan · deploy</p>
            <div class="badges">
                <span class="badge"><span class="badge-dot"></span> <strong>{{ env }}</strong></span>
                <span class="badge">build · <strong>{{ build }}</strong></span>
                <span class="badge">pod · <strong>{{ pod }}</strong></span>
            </div>
        </div>

        <div class="card">
            <h2>Deployment Status</h2>
            <div class="status-grid" id="status">
                <div class="status-item"><div class="status-label">Loading</div><div class="status-value pulse">···</div></div>
            </div>
        </div>

        <div class="card">
            <h2>Demo Database (SQLite)</h2>
            <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 16px;">
                Add a contact, then delete the pod to test persistence (lab 3-9 vs 4-1).
            </p>
            <form id="add-form">
                <input name="name" placeholder="Name" required>
                <input name="phone" placeholder="Phone" required>
                <button type="submit">Add Contact</button>
            </form>

            <div style="margin-top: 20px; overflow-x: auto;">
                <table>
                    <thead>
                        <tr><th>ID</th><th>Name</th><th>Phone</th><th style="text-align:right;">Action</th></tr>
                    </thead>
                    <tbody id="contacts-body">
                        <tr><td colspan="4" class="empty">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">Jaden Rogers · CIT 225 · Spring 2026</div>
    </div>

<script>
async function loadContacts() {
    const res = await fetch('/api/contacts');
    const data = await res.json();
    const body = document.getElementById('contacts-body');
    if (data.length === 0) {
        body.innerHTML = '<tr><td colspan="4" class="empty">No contacts yet. Add one above.</td></tr>';
        return;
    }
    body.innerHTML = data.map(c =>
        `<tr>
            <td class="id-cell">#${c.id}</td>
            <td>${c.name}</td>
            <td>${c.phone}</td>
            <td style="text-align:right;"><button class="delete-btn" onclick="del(${c.id})">Delete</button></td>
        </tr>`
    ).join('');
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
    document.getElementById('status').innerHTML = `
        <div class="status-item">
            <div class="status-label">Status</div>
            <div class="status-value live"><span class="badge-dot"></span>RUNNING</div>
        </div>
        <div class="status-item">
            <div class="status-label">Build</div>
            <div class="status-value">${data.build}</div>
        </div>
        <div class="status-item">
            <div class="status-label">Environment</div>
            <div class="status-value">${data.env}</div>
        </div>
        <div class="status-item">
            <div class="status-label">Pod</div>
            <div class="status-value">${data.pod}</div>
        </div>
        <div class="status-item">
            <div class="status-label">Uptime</div>
            <div class="status-value">${data.uptime}s</div>
        </div>
    `;
}

loadContacts();
loadStatus();
setInterval(loadContacts, 3000);
setInterval(loadStatus, 5000);
</script>
</body>
</html>
"""

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
