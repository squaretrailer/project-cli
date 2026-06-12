class Project:
    _next_id = 1

    def __init__(self, title, owner_id, description="", due_date="", project_id=None):
        self.title = title
        self.owner_id = owner_id
        self.description = description
        self.due_date = due_date
        if project_id is not None:
            self._id = project_id
            if project_id >= Project._next_id:
                Project._next_id = project_id + 1
        else:
            self._id = Project._next_id
            Project._next_id += 1
        self._task_ids = []

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
            raise ValueError("Project title cannot be empty")
        self._title = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if value and not (len(value) == 10 and value[4] == "-" and value[7] == "-"):
            raise ValueError("Due date must be YYYY-MM-DD")
        self._due_date = value

    @property
    def task_ids(self):
        return self._task_ids.copy()

    def add_task(self, tid):
        if tid not in self._task_ids:
            self._task_ids.append(tid)

    def remove_task(self, tid):
        self._task_ids = [t for t in self._task_ids if t != tid]

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self.description,
            "due_date": self._due_date,
            "owner_id": self.owner_id,
            "task_ids": self._task_ids,
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(
            title=data["title"],
            owner_id=data["owner_id"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            project_id=data["id"],
        )
        p._task_ids = data.get("task_ids", [])
        return p

    def __str__(self):
        return f"[{self.id}] {self.title}"