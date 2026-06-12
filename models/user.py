class User:
    _next_id = 1

    def __init__(self, name, email, user_id=None):
        self.name = name
        self.email = email
        if user_id is not None:
            self._id = user_id
            if user_id >= User._next_id:
                User._next_id = user_id + 1
        else:
            self._id = User._next_id
            User._next_id += 1
        self._project_ids = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        value = value.strip().lower()
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email")
        self._email = value

    @property
    def project_ids(self):
        return self._project_ids.copy()

    def add_project(self, pid):
        if pid not in self._project_ids:
            self._project_ids.append(pid)

    def remove_project(self, pid):
        self._project_ids = [p for p in self._project_ids if p != pid]

    def to_dict(self):
        return {"id": self._id, "name": self._name, "email": self._email, "project_ids": self._project_ids}

    @classmethod
    def from_dict(cls, data):
        u = cls(data["name"], data["email"], user_id=data["id"])
        u._project_ids = data.get("project_ids", [])
        return u

    def __str__(self):
        return f"[{self.id}] {self.name} <{self.email}>"