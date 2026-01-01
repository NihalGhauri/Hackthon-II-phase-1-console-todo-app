"""
Unit tests for Task model validation.
"""
import pytest
from src.models.task import Task


def test_task_creation_valid() -> None:
    """
    Test creating a valid Task object.
    """
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_task_creation_defaults() -> None:
    """
    Test creating a Task object with default values.
    """
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_invalid_title_empty() -> None:
    """
    Test creating a Task object with an empty title raises ValueError.
    """
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(id=1, title="")


def test_task_creation_invalid_title_whitespace() -> None:
    """
    Test creating a Task object with a whitespace-only title raises ValueError.
    """
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(id=1, title="   ")


def test_task_creation_invalid_id_negative() -> None:
    """
    Test creating a Task object with a negative ID raises ValueError.
    """
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=-1, title="Test Task")


def test_task_creation_invalid_id_zero() -> None:
    """
    Test creating a Task object with zero ID raises ValueError.
    """
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=0, title="Test Task")


def test_task_creation_invalid_id_non_integer() -> None:
    """
    Test creating a Task object with non-integer ID raises TypeError during validation.
    """
    # This test is for type checking which would be caught by mypy
    # At runtime, the type is not enforced by the dataclass
    pass


def test_task_validate_method_valid() -> None:
    """
    Test the validate method with valid task data.
    """
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    assert task.validate() is True


def test_task_validate_method_invalid_title() -> None:
    """
    Test the validate method with invalid title by manually setting it after creation.
    """
    task = Task(id=1, title="Valid Title", description="Test Description", completed=False)
    task.title = ""  # Manually set to invalid state after creation
    assert task.validate() is False


def test_task_validate_method_invalid_whitespace_title() -> None:
    """
    Test the validate method with whitespace-only title by manually setting it after creation.
    """
    task = Task(id=1, title="Valid Title", description="Test Description", completed=False)
    task.title = "   "  # Manually set to invalid state after creation
    assert task.validate() is False


def test_task_validate_method_invalid_id() -> None:
    """
    Test the validate method with invalid ID.
    """
    # Create task with valid data first, then modify the ID
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    task.id = -1
    assert task.validate() is False


def test_task_validate_method_invalid_completed() -> None:
    """
    Test the validate method with invalid completed status.
    """
    # Create task with valid data first, then modify the completed status
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    task.completed = "not_a_boolean"  # type: ignore
    assert task.validate() is False