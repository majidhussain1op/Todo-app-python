import click
import json
import os

TODO_FILE = "todo.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TODO_FILE):  
        return []  # Fix: Return an empty list if file doesn't exist

    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@click.command()  # Fix: Changed from `click.Command()` to `@click.command()`
@click.argument("task")
def add(task):
    """Add a task to the list"""
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})  # Fix: Corrected key name from "tasks" to "task"
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")

@click.command()
def list():
    """List all the task"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    for index, task in enumerate(tasks, 1):
        status = "✅" if task['done'] else "❌"
        click.echo(f"{index}, {task['task']} [{status}]")

@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as complete"""
    tasks = load_tasks()

    if not tasks:  # Ensure tasks list is not empty
        click.echo("❌ No tasks found. Add a task first.")
        return

    if 1 <= task_number <= len(tasks):  # Ensure task_number is valid
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"✅ Task {task_number} marked as completed.")
    else:
        click.echo(f"❌ Invalid task number: {task_number}. Please enter a valid number.")


@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()

    if not tasks:  # Ensure tasks list is not empty
        click.echo("❌ No tasks found. Add a task first.")
        return

    if 1 <= task_number <= len(tasks):  # Ensure task_number is valid
        removed_task = tasks.pop(task_number - 1)  # Remove task
        save_tasks(tasks)
        click.echo(f"🗑 Task removed: {removed_task}")
    else:
        click.echo("⚠️ Invalid task number. Please enter a valid task ID.")






# Register the command
cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)



if __name__ == "__main__":
    cli()
