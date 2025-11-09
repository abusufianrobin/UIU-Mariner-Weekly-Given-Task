import json
import os

TODO_FILE = "tasks.json"


class TaskNotFoundError(Exception):
    """Custom exception when a task is not found."""
    pass


def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def show_tasks(tasks):
    """Display all current tasks."""
    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\nTo-Do List:")
        for i, task in enumerate(tasks, 1):
            status = "Done!!!" if task["done"] else "Pending!!!"
            print(f"{i}. {task['title']} — {status}")

def add_task(tasks):
    """Add a new task."""
    title = input("Enter the task title: ").strip()
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        print(f'Task "{title}" added successfully!')
    else:
        print("Task title cannot be empty.")


def mark_done(tasks):

    """Mark a task as completed."""
    show_tasks(tasks)
    try:
        num = int(input("\nEnter task number to mark as done: "))
        if num < 1 or num > len(tasks):

            raise TaskNotFoundError("Invalid task number.")
        
        tasks[num - 1]["done"] = True

        save_tasks(tasks)
        print(f"Task '{tasks[num - 1]['title']}' marked as done!")

    except ValueError:

        print("Please enter a valid number.")
    except TaskNotFoundError as e:
        print(f"{e}")


def delete_task(tasks):

    """Delete a task by its number."""
    show_tasks(tasks)
    try:

        num = int(input("\nEnter task number to delete: "))

        if num < 1 or num > len(tasks):

            raise TaskNotFoundError("Invalid task number.")
        removed = tasks.pop(num - 1)
        save_tasks(tasks)
        print(f"Task '{removed['title']}' deleted successfully!")

    except ValueError:
        
        print("Please enter a valid number.")
    except TaskNotFoundError as e:
        print(f"{e}")

