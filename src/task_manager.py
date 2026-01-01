"""
Task management class with CRUD operations for the console todo app.
"""
from typing import List, Optional
from .models.task import Task


class TaskManager:
    """
    Handles the in-memory collection of Task entities with CRUD operations.
    """
    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task list and next ID counter.
        """
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Adds a new task to the in-memory list with an auto-generated ID.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty or contain only whitespace")

        task = Task(id=self._next_id, title=title, description=description)
        self.tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        """
        Returns a list of all tasks in the in-memory collection.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Updates an existing task's details by ID.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object if found, None otherwise

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        if title is not None:
            if not title or title.strip() == "":
                raise ValueError("Task title cannot be empty or contain only whitespace")
            task.title = title

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggles the completion status of a task by its ID.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if found, None otherwise
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        return task

    def get_next_id(self) -> int:
        """
        Returns the next available ID for a new task.

        Returns:
            The next ID that will be assigned to a new task
        """
        return self._next_id