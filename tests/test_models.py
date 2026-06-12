import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.user import User
from models.project import Project
from models.task import Task

@pytest.fixture(autouse=True)
def reset_ids():
    # Reset class-level ID counters before each test
    User._next_id = 1
    Project._next_id = 1
    Task._next_id = 1
    yield

def test_user_creation():
    u = User("Alice", "alice@test.com")
    assert u.name == "Alice"
    assert u.email == "alice@test.com"

def test_user_auto_id():
    u1 = User("Bob", "b@t.c")
    u2 = User("Carol", "c@t.c")
    assert u1.id == 1
    assert u2.id == 2

def test_project_validation():
    p = Project("My Project", owner_id=1)
    p.title = "New Title"
    assert p.title == "New Title"
    with pytest.raises(ValueError):
        p.title = "   "

def test_task_status():
    t = Task("Do something", project_id=1)
    assert t.status == "todo"
    t.start()
    assert t.status == "in_progress"
    t.complete()
    assert t.status == "done"