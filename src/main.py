"""
Console todo application main entry point with menu-driven interface.
"""
import sys
from typing import Optional
from .task_manager import TaskManager


def display_menu() -> None:
    """
    Displays the main menu options to the user.
    """
    print("\n====> Console Todo App <====")
    print("-----------------------------")
    print("1. Add task")
    print("2. List tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Complete task")
    print("6. Exit")
    print("-----------------------------")


def get_user_choice() -> str:
    """
    Prompts the user for menu selection and returns their choice.

    Returns:
        The user's menu choice as a string
    """
    try:
        choice = input("Enter your choice (1-6): ").strip()
        return choice
    except (EOFError, KeyboardInterrupt):
        print("\nExiting application...")
        sys.exit(0)


def add_task_ui(task_manager: TaskManager) -> None:
    """
    Handles the UI for adding a new task.

    Args:
        task_manager: The TaskManager instance to use for operations
    """
    print("\n==> Add New Task <==")
    try:
        title = input("Enter task title: ").strip()
        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description (optional): ").strip()
        task = task_manager.add_task(title, description)
        print(f"Task added successfully with ID: {task.id}")
    except ValueError as e:
        print(f"Error: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


def list_tasks_ui(task_manager: TaskManager) -> None:
    """
    Handles the UI for listing all tasks.

    Args:
        task_manager: The TaskManager instance to use for operations
    """
    print("\n--- Task List ---")
    tasks = task_manager.list_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✔" if task.completed else "○"
        print(f"{status} [{task.id}] {task.title}")
        if task.description:
            print(f"    Description: {task.description}")
        print()


def update_task_ui(task_manager: TaskManager) -> None:
    """
    Handles the UI for updating an existing task.

    Args:
        task_manager: The TaskManager instance to use for operations
    """
    print("\n--- Update Task ---")
    try:
        task_id_str = input("Enter task ID to update: ").strip()
        task_id = int(task_id_str)

        task = task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {task.title}")
        if task.description:
            print(f"Current description: {task.description}")

        new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
        new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

        # Use None to indicate no change, or the new value if provided
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        updated_task = task_manager.update_task(task_id, title_to_update, description_to_update)
        if updated_task:
            print(f"Task {task_id} updated successfully.")
        else:
            print(f"Error: Failed to update task {task_id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


def delete_task_ui(task_manager: TaskManager) -> None:
    """
    Handles the UI for deleting a task.

    Args:
        task_manager: The TaskManager instance to use for operations
    """
    print("\n--- Delete Task ---")
    try:
        task_id_str = input("Enter task ID to delete: ").strip()
        task_id = int(task_id_str)

        success = task_manager.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
    except ValueError:
        print(f"Error: Invalid task ID '{task_id_str}'. Please enter a number.")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


def complete_task_ui(task_manager: TaskManager) -> None:
    """
    Handles the UI for toggling a task's completion status.

    Args:
        task_manager: The TaskManager instance to use for operations
    """
    print("\n--- Complete Task ---")
    try:
        task_id_str = input("Enter task ID to toggle completion: ").strip()
        task_id = int(task_id_str)

        task = task_manager.toggle_task_completion(task_id)
        if task:
            status = "completed" if task.completed else "incomplete"
            print(f"Task {task_id} marked as {status}.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
    except ValueError:
        print(f"Error: Invalid task ID '{task_id_str}'. Please enter a number.")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


def main() -> None:
    """
    Main application loop that handles user interaction.
    """
    task_manager = TaskManager()
    print("Welcome to the Console Todo App!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            add_task_ui(task_manager)
        elif choice == "2":
            list_tasks_ui(task_manager)
        elif choice == "3":
            update_task_ui(task_manager)
        elif choice == "4":
            delete_task_ui(task_manager)
        elif choice == "5":
            complete_task_ui(task_manager)
        elif choice == "6":
            print("Thank you for using the Console Todo App. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
