import sys, os, tempfile, shutil
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.tracker import Tracker
import utils.storage as storage

@pytest.fixture(autouse=True)
def reset_ids():
    # Reset class-level ID counters before each test to avoid side effects
    from models.user import User
    from models.project import Project
    from models.task import Task
    User._next_id = 1
    Project._next_id = 1
    Task._next_id = 1
    yield

def test_full_flow():
    # use a temporary data directory
    original_data_dir = storage.DATA_DIR
    temp_dir = Path(tempfile.mkdtemp())  # convert to Path
    storage.DATA_DIR = temp_dir
    storage.USERS_FILE = storage.DATA_DIR / "users.json"
    storage.PROJECTS_FILE = storage.DATA_DIR / "projects.json"
    storage.TASKS_FILE = storage.DATA_DIR / "tasks.json"

    tracker = Tracker()
    u = tracker.add_user("TestUser", "test@ex.com")
    assert u.id == 1

    p = tracker.add_project("TestProj", "TestUser", "desc", "2025-12-31")
    assert p.title == "TestProj"

    t = tracker.add_task("TestTask", "TestProj", "me", "todo")
    assert t.title == "TestTask"

    tracker.complete_task("TestTask")
    t2 = tracker.get_task("TestTask")
    assert t2.status == "done"

    # cleanup
    shutil.rmtree(temp_dir)
    storage.DATA_DIR = original_data_dir