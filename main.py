#!/usr/bin/env python3
import argparse
import sys
from core.tracker import Tracker
from utils.display import banner, print_users, print_projects, print_tasks, success, error, info

def main():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # User commands
    p = subparsers.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p = subparsers.add_parser("list-users", help="Show all users")
    p = subparsers.add_parser("delete-user", help="Delete a user and all their data")
    p.add_argument("--user", required=True)
    p.add_argument("--yes", "-y", action="store_true")

    # Project commands
    p = subparsers.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--desc", default="")
    p.add_argument("--due-date", default="")
    p = subparsers.add_parser("list-projects", help="List projects (optionally for a user)")
    p.add_argument("--user", default=None)
    p = subparsers.add_parser("delete-project", help="Delete a project and its tasks")
    p.add_argument("--project", required=True)
    p.add_argument("--yes", "-y", action="store_true")

    # Task commands
    p = subparsers.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assign", default="")
    p.add_argument("--status", default="todo", choices=["todo", "in_progress", "done"])
    p = subparsers.add_parser("list-tasks", help="List tasks (optionally for a project)")
    p.add_argument("--project", default=None)
    p = subparsers.add_parser("complete-task", help="Mark a task as done")
    p.add_argument("--task", required=True)
    p.add_argument("--project", default=None)
    p = subparsers.add_parser("start-task", help="Mark a task as in progress")
    p.add_argument("--task", required=True)
    p.add_argument("--project", default=None)
    p = subparsers.add_parser("delete-task", help="Delete a task")
    p.add_argument("--task", required=True)
    p.add_argument("--project", default=None)

    args = parser.parse_args()
    tracker = Tracker()
    banner()

    try:
        if args.command == "add-user":
            u = tracker.add_user(args.name, args.email)
            success(f"User created: {u.name} (ID {u.id})")
        elif args.command == "list-users":
            print_users(tracker.list_users())
        elif args.command == "delete-user":
            u = tracker.get_user(args.user)
            if not u:
                error(f"User '{args.user}' not found")
                return 1
            if not args.yes:
                ans = input(f"Delete '{u.name}' and all their data? (y/N): ")
                if ans.lower() not in ("y", "yes"):
                    info("Cancelled")
                    return 0
            tracker.delete_user(args.user)
            success(f"User '{u.name}' deleted")
        elif args.command == "add-project":
            p = tracker.add_project(args.title, args.user, args.desc, args.due_date)
            success(f"Project created: '{p.title}' (ID {p.id}) for user {args.user}")
        elif args.command == "list-projects":
            projs = tracker.list_projects(args.user)
            print_projects(projs, args.user or "")
        elif args.command == "delete-project":
            p = tracker.get_project(args.project)
            if not p:
                error(f"Project '{args.project}' not found")
                return 1
            if not args.yes:
                ans = input(f"Delete project '{p.title}' and all its tasks? (y/N): ")
                if ans.lower() not in ("y", "yes"):
                    info("Cancelled")
                    return 0
            tracker.delete_project(args.project)
            success(f"Project '{p.title}' deleted")
        elif args.command == "add-task":
            t = tracker.add_task(args.title, args.project, args.assign, args.status)
            success(f"Task added: '{t.title}' (ID {t.id}) in project '{args.project}'")
        elif args.command == "list-tasks":
            tasks = tracker.list_tasks(args.project)
            print_tasks(tasks, args.project or "")
        elif args.command == "complete-task":
            t = tracker.complete_task(args.task, args.project)
            success(f"Task '{t.title}' marked as DONE")
        elif args.command == "start-task":
            t = tracker.start_task(args.task, args.project)
            success(f"Task '{t.title}' marked as IN PROGRESS")
        elif args.command == "delete-task":
            t = tracker.get_task(args.task, args.project)
            if not t:
                error(f"Task '{args.task}' not found")
                return 1
            tracker.delete_task(args.task, args.project)
            success(f"Task '{t.title}' deleted")
    except Exception as e:
        error(str(e))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
