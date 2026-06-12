class Task:
    _next_id = 1
    STATUSES = ["todo", "in_progress", "done"]
    def __init__(self, title, project_id, assigned_to="", status="todo", task_id=None):
        self.title = title
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.status = status
        if task_id is not None:
            self._id = task_id
            if task_id >= Task._next_id:
                Task._next_id = task_id + 1
        else:
            self._id = Task._next_id
            Task._next_id += 1
    @property
    def id(self):
        return self._id
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty")
        self._title = value
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        if value not in Task.STATUSES:
            raise ValueError(f"Status must be one of {Task.STATUSES}")
        self._status = value
    def complete(self):
        self.status = "done"
    def start(self):
        self.status = "in_progress"
    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "status": self._status,
            "assigned_to": self.assigned_to,
            "project_id": self.project_id,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            project_id=data["project_id"],
            assigned_to=data.get("assigned_to", ""),
            status=data.get("status", "todo"),
            task_id=data["id"],
        )
    def __str__(self):
        return f"[{self.id}] {self.title} [{self.status}]"
