from models import User, Project, Task
from utils.storage import load_users, save_users, load_projects, save_projects, load_tasks, save_tasks

class Tracker:
    def __init__(self):
        self._users = []
        self._projects = []
        self._tasks = []
        self._load_all()

    def _load_all(self):
        self._users = [User.from_dict(d) for d in load_users()]
        self._projects = [Project.from_dict(d) for d in load_projects()]
        self._tasks = [Task.from_dict(d) for d in load_tasks()]

    def _save_all(self):
        save_users(self._users)
        save_projects(self._projects)
        save_tasks(self._tasks)

    # ----- User operations -----
    def add_user(self, name, email):
        email = email.strip().lower()
        if any(u.email == email for u in self._users):
            raise ValueError(f"User with email {email} already exists")
        u = User(name, email)
        self._users.append(u)
        self._save_all()
        return u

    def list_users(self):
        return self._users.copy()

    def get_user(self, identifier):
        if str(identifier).isdigit():
            uid = int(identifier)
            for u in self._users:
                if u.id == uid:
                    return u
        else:
            name = str(identifier).lower()
            for u in self._users:
                if u.name.lower() == name:
                    return u
        return None

    def delete_user(self, identifier):
        user = self.get_user(identifier)
        if not user:
            raise ValueError(f"User '{identifier}' not found")
        for pid in user.project_ids:
            self._delete_project_by_id(pid)
        self._users = [u for u in self._users if u.id != user.id]
        self._save_all()
        return user

    # ----- Project operations -----
    def add_project(self, title, user_identifier, description="", due_date=""):
        owner = self.get_user(user_identifier)
        if not owner:
            raise ValueError(f"User '{user_identifier}' not found")
        # check duplicate title for this user
        for p in self._projects:
            if p.owner_id == owner.id and p.title.lower() == title.lower():
                raise ValueError(f"User already has a project named '{title}'")
        proj = Project(title, owner.id, description, due_date)
        self._projects.append(proj)
        owner.add_project(proj.id)
        self._save_all()
        return proj

    def list_projects(self, user_identifier=None):
        if user_identifier is None:
            return self._projects.copy()
        user = self.get_user(user_identifier)
        if not user:
            raise ValueError(f"User '{user_identifier}' not found")
        return [p for p in self._projects if p.owner_id == user.id]

    def get_project(self, identifier):
        if str(identifier).isdigit():
            pid = int(identifier)
            for p in self._projects:
                if p.id == pid:
                    return p
        else:
            title = str(identifier).lower()
            for p in self._projects:
                if p.title.lower() == title:
                    return p
        return None

    def _delete_project_by_id(self, pid):
        proj = self.get_project(pid)
        if not proj:
            return
        # delete its tasks
        self._tasks = [t for t in self._tasks if t.project_id != pid]
        # remove from owner
        owner = self.get_user(proj.owner_id)
        if owner:
            owner.remove_project(pid)
        # remove project
        self._projects = [p for p in self._projects if p.id != pid]
        self._save_all()

    def delete_project(self, identifier):
        proj = self.get_project(identifier)
        if not proj:
            raise ValueError(f"Project '{identifier}' not found")
        self._delete_project_by_id(proj.id)
        return proj

    # ----- Task operations -----
    def add_task(self, title, project_identifier, assigned_to="", status="todo"):
        proj = self.get_project(project_identifier)
        if not proj:
            raise ValueError(f"Project '{project_identifier}' not found")
        task = Task(title, proj.id, assigned_to, status)
        self._tasks.append(task)
        proj.add_task(task.id)
        self._save_all()
        return task

    def list_tasks(self, project_identifier=None):
        if project_identifier is None:
            return self._tasks.copy()
        proj = self.get_project(project_identifier)
        if not proj:
            raise ValueError(f"Project '{project_identifier}' not found")
        return [t for t in self._tasks if t.project_id == proj.id]

    def get_task(self, identifier, project_identifier=None):
        if str(identifier).isdigit():
            tid = int(identifier)
            for t in self._tasks:
                if t.id == tid:
                    return t
        else:
            title = str(identifier).lower()
            for t in self._tasks:
                if t.title.lower() == title:
                    if project_identifier:
                        proj = self.get_project(project_identifier)
                        if proj and t.project_id == proj.id:
                            return t
                    else:
                        return t
        return None

    def complete_task(self, identifier, project_identifier=None):
        task = self.get_task(identifier, project_identifier)
        if not task:
            raise ValueError(f"Task '{identifier}' not found")
        task.complete()
        self._save_all()
        return task

    def start_task(self, identifier, project_identifier=None):
        task = self.get_task(identifier, project_identifier)
        if not task:
            raise ValueError(f"Task '{identifier}' not found")
        task.start()
        self._save_all()
        return task

    def delete_task(self, identifier, project_identifier=None):
        task = self.get_task(identifier, project_identifier)
        if not task:
            raise ValueError(f"Task '{identifier}' not found")
        proj = self.get_project(task.project_id)
        if proj:
            proj.remove_task(task.id)
        self._tasks = [t for t in self._tasks if t.id != task.id]
        self._save_all()
        return task