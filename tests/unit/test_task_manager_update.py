"""
Unit tests specifically for TaskManager update_task method.
"""
import pytest
from src.task_manager import TaskManager


def test_update_task_valid_title_and_description() -> None:
    """
    Test updating both title and description of a task.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    updated_task = manager.update_task(original_task.id, "Updated Task", "Updated Description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed == original_task.completed  # Should remain unchanged

    # Verify the task in the manager's list is also updated
    task_in_list = manager.get_task_by_id(original_task.id)
    assert task_in_list is not None
    assert task_in_list.title == "Updated Task"


def test_update_task_title_only() -> None:
    """
    Test updating only the title of a task.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    updated_task = manager.update_task(original_task.id, "Updated Task")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Original Description"  # Should remain unchanged


def test_update_task_description_only() -> None:
    """
    Test updating only the description of a task.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    updated_task = manager.update_task(original_task.id, description="Updated Description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "Original Task"  # Should remain unchanged
    assert updated_task.description == "Updated Description"


def test_update_task_not_found() -> None:
    """
    Test updating a task that doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    result = manager.update_task(999, "Updated Task")
    assert result is None
    assert len(manager.tasks) == 1  # No changes to the list


def test_update_task_invalid_title_empty() -> None:
    """
    Test updating a task with an empty title raises ValueError.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.update_task(original_task.id, "")


def test_update_task_invalid_title_whitespace() -> None:
    """
    Test updating a task with a whitespace-only title raises ValueError.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.update_task(original_task.id, "   ")


def test_update_task_with_none_values() -> None:
    """
    Test updating a task with None values (should not change anything).
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    # This should not update anything since None means "no change"
    updated_task = manager.update_task(original_task.id, None, None)

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "Original Task"
    assert updated_task.description == "Original Description"


def test_update_task_multiple_tasks() -> None:
    """
    Test updating a specific task among multiple tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Update only task2
    updated_task = manager.update_task(task2.id, "Updated Task 2", "Updated Description 2")

    assert updated_task is not None
    assert updated_task.id == task2.id
    assert updated_task.title == "Updated Task 2"
    assert updated_task.description == "Updated Description 2"

    # Verify other tasks remain unchanged
    task1_in_list = manager.get_task_by_id(task1.id)
    task3_in_list = manager.get_task_by_id(task3.id)
    assert task1_in_list is not None
    assert task1_in_list.title == "Task 1"
    assert task3_in_list is not None
    assert task3_in_list.title == "Task 3"


def test_update_task_preserves_completion_status() -> None:
    """
    Test that updating a task preserves its completion status.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")
    # Toggle to mark as complete
    manager.toggle_task_completion(original_task.id)

    # Update the task
    updated_task = manager.update_task(original_task.id, "Updated Task")

    assert updated_task is not None
    assert updated_task.completed is True  # Should remain True