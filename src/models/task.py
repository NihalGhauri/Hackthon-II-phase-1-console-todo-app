"""
Task model representing a single todo item in the application.
"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo item in the application.

    Attributes:
        id: Unique identifier (auto-incrementing, starts from 1)
        title: Short description of the task (required)
        description: Detailed explanation of the task (optional, can be empty string)
        completed: Completion status (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """
        Validates the Task object after initialization.

        Raises:
            ValueError: If title is empty or contains only whitespace,
                      or if ID is not a positive integer
        """
        if not self.title or self.title.strip() == "":
            raise ValueError("Task title cannot be empty or contain only whitespace")

        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")

    def validate(self) -> bool:
        """
        Validates the Task object state.

        Returns:
            True if the task is valid, False otherwise
        """
        if not self.title or self.title.strip() == "":
            return False

        if not isinstance(self.id, int) or self.id <= 0:
            return False

        if not isinstance(self.completed, bool):
            return False

        return True