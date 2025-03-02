from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DB_FILE = "tasks.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )''')

@app.route('/')
def index():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get("task")
    if task:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    return redirect(url_for("index"))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

