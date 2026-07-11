"""
DecodeLabs Internship - Task 1: TO-DO LIST
--------------------------------------------
Goal: Build a program where users can add tasks to a list and view them.
Key Skill: Lists (append & print loops).

This follows the IPO model taught in the guide:
    Input   -> user enters a task
    Process -> task is appended to the list (stored as a dictionary,
               like a "row" in a database table)
    Output  -> tasks are displayed back to the user in a loop

Each task is stored as a dictionary: {"id": <int>, "task": <str>, "done": <bool>}
The overall collection of tasks is a LIST of these dictionaries,
mirroring how a database table is a list of rows.
"""

import json
import os

FILE_NAME = "tasks.json"   # used for persistence (saving beyond RAM)

# -------------------- IPO: Persistence helpers --------------------

def load_tasks():
    """Load tasks from file if it exists, otherwise start with an empty list."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save the current list of tasks to a file (moves data from RAM to disk)."""
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)


# -------------------- Core Logic --------------------

def add_task(tasks, task_name):
    """Append a new task (dictionary) to the tasks list. O(1) amortized."""
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    task = {"id": new_id, "task": task_name, "done": False}
    tasks.append(task)
    print(f"Task added: '{task_name}'")


def view_tasks(tasks):
    """Print every task in the list using a print loop."""
    if not tasks:
        print("📭 Your to-do list is empty.")
        return

    print("\n--- YOUR TO-DO LIST ---")
    for task in tasks:
        status = "✔ Done" if task["done"] else "❌ Pending"
        print(f"[{task['id']}] {task['task']}  -  {status}")
    print("-----------------------\n")


def complete_task(tasks, task_id):
    """Mark a task as done by its id."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            print(f"🎉 Task {task_id} marked as done!")
            return
    print("⚠️ Task ID not found.")


def delete_task(tasks, task_id):
    """Remove a task from the list by its id."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print(f"🗑️ Task {task_id} deleted.")
            return
    print("⚠️ Task ID not found.")


# -------------------- Main Program (Input/Output loop) --------------------

def main():
    tasks = load_tasks()  # start by restoring any saved tasks

    menu = """
========= DECODELABS TO-DO LIST =========
1. Add Task
2. View Tasks
3. Mark Task as Done
4. Delete Task
5. Exit
==========================================
"""

    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            task_name = input("Enter the task: ").strip()
            if task_name:
                add_task(tasks, task_name)
                save_tasks(tasks)
            else:
                print("⚠️ Task cannot be empty.")

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            try:
                task_id = int(input("Enter task ID to mark as done: "))
                complete_task(tasks, task_id)
                save_tasks(tasks)
            except ValueError:
                print("⚠️ Please enter a valid number.")

        elif choice == "4":
            view_tasks(tasks)
            try:
                task_id = int(input("Enter task ID to delete: "))
                delete_task(tasks, task_id)
                save_tasks(tasks)
            except ValueError:
                print("⚠️ Please enter a valid number.")

        elif choice == "5":
            print("👋 Goodbye! Your tasks have been saved.")
            break

        else:
            print("⚠️ Invalid choice, please select 1-5.")


if __name__ == "__main__":
    main()