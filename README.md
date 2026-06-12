# Project Tracker CLI

A simple command-line tool to manage users, projects, and tasks.  
Data is stored in JSON files. Uses `tabulate` and `colorama`.

## Installation

```bash
pip install -r requirements.txt

```

# User Commands
python main.py add-user --name "Alice" --email "alice@example.com"
python main.py list-users
python main.py delete-user --user Alice
python main.py delete-user --user Alice --yes


# Project Commands
python main.py add-project --user Alice --title "My Project" --desc "Learn CLI" --due-date 2025-12-31
python main.py list-projects
python main.py list-projects --user Alice
python main.py delete-project --project "My Project"
python main.py delete-project --project "My Project" --yes

# Task Commands
python main.py add-task --project "My Project" --title "Write code" --assign Alice --status todo
python main.py list-tasks
python main.py list-tasks --project "My Project"
python main.py start-task --task "Write code"
python main.py complete-task --task "Write code"
python main.py delete-task --task "Write code"


# Help
python main.py --help
python main.py add-user --help