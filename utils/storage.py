import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"

def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def _read_json(path):
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def _write_json(path, data):
    _ensure_dir()
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def load_users():
    return _read_json(USERS_FILE)

def save_users(users):
    _write_json(USERS_FILE, [u.to_dict() for u in users])

def load_projects():
    return _read_json(PROJECTS_FILE)

def save_projects(projects):
    _write_json(PROJECTS_FILE, [p.to_dict() for p in projects])

def load_tasks():
    return _read_json(TASKS_FILE)

def save_tasks(tasks):
    _write_json(TASKS_FILE, [t.to_dict() for t in tasks])