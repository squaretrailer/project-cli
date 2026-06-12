from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

def print_users(users):
    if not users:
        print(f"{Fore.YELLOW}No users found.{Style.RESET_ALL}")
        return
    headers = ["ID", "Name", "Email", "Projects"]
    rows = [[u.id, u.name, u.email, len(u.project_ids)] for u in users]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_projects(projects, owner_name=""):
    if not projects:
        print(f"{Fore.YELLOW}No projects found.{Style.RESET_ALL}")
        return
    headers = ["ID", "Title", "Description", "Due Date", "Tasks"]
    rows = [[p.id, p.title, p.description[:30], p.due_date or "-", len(p.task_ids)] for p in projects]
    title = f"Projects for {owner_name}" if owner_name else "All Projects"
    print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_tasks(tasks, project_title=""):
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return
    headers = ["ID", "Title", "Status", "Assigned To"]
    rows = [[t.id, t.title, t.status.upper(), t.assigned_to or "-"] for t in tasks]
    title = f"Tasks in '{project_title}'" if project_title else "All Tasks"
    print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def success(msg):
    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")

def error(msg):
    print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def info(msg):
    print(f"{Fore.BLUE}ℹ {msg}{Style.RESET_ALL}")

def banner():
    print(f"{Fore.MAGENTA}{'='*50}")
    print(f"{Fore.CYAN}  PROJECT TRACKER CLI")
    print(f"{Fore.YELLOW}  Manage users, projects, tasks")
    print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}\n")