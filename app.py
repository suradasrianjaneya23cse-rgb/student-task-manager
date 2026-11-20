from flask import Flask, request, redirect, render_template_string
import json
import os
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(os.environ.get("TASKS_FILE", Path(__file__).with_name("tasks.json")))

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Student Task Manager</title>
<style>
* { box-sizing: border-box; }
body { font-family: Arial, sans-serif; background: #f1f5f9; margin: 0; padding: 40px 16px; color: #1e293b; }
.container { max-width: 650px; margin: auto; background: white; padding: 28px; border-radius: 14px; box-shadow: 0 8px 24px rgba(15,23,42,.08); }
h1 { text-align: center; color: #2563eb; margin-top: 0; }
.subtitle { text-align: center; color: #64748b; }
.add-form { display: flex; gap: 10px; margin: 24px 0; }
input { flex: 1; min-width: 0; padding: 12px; border: 1px solid #cbd5e1; border-radius: 7px; font-size: 15px; }
button { border: 0; border-radius: 7px; padding: 11px 15px; background: #2563eb; color: white; cursor: pointer; }
ul { list-style: none; padding: 0; }
li { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 13px; margin: 10px 0; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; }
.completed { text-decoration: line-through; color: #94a3b8; }
.actions { display: flex; gap: 12px; white-space: nowrap; }
a { color: #2563eb; text-decoration: none; }
a.delete { color: #dc2626; }
.empty { text-align: center; color: #64748b; }
@media (max-width: 480px) { .add-form { flex-direction: column; } li { align-items: flex-start; flex-direction: column; } }
</style>
</head>
<body>
<main class="container">
<h1>Student Task Manager</h1>
<p class="subtitle">Organize your study tasks in one place.</p>
<form class="add-form" action="/add" method="POST">
<input type="text" name="task" placeholder="Enter a task..." maxlength="200" required>
<button type="submit">Add Task</button>
</form>
<h3>My Tasks</h3>
<ul>
{% for task in tasks %}
<li>
<span class="{{ 'completed' if task.done else '' }}">{{ task.name }}</span>
<div class="actions">
<a href="/complete/{{ loop.index0 }}">{{ 'Undo' if task.done else 'Mark done' }}</a>
<a class="delete" href="/delete/{{ loop.index0 }}">Delete</a>
</div>
</li>
{% else %}
<li class="empty">No tasks yet. Add your first task!</li>
{% endfor %}
</ul>
</main>
</body>
</html>
"""

def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def home():
    return render_template_string(HTML, tasks=load_tasks())

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("task", "").strip()
    if name:
        tasks = load_tasks()
        tasks.append({"name": name[:200], "done": False})
        save_tasks(tasks)
    return redirect("/")

@app.route("/complete/<int:index>")
def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index].get("done", False)
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
