"""
Unit tests for TaskManager class.
"""
import pytest
from src.task_manager import TaskManager
from src.models.task import Task


def test_task_manager_initialization() -> None:
    """
    Test TaskManager initialization.
    """
    manager = TaskManager()
    assert manager.tasks == []
    assert manager._next_id == 1


def test_add_task_valid() -> None:
    """
    Test adding a valid task to the manager.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Test Description")

    assert len(manager.tasks) == 1
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert manager._next_id == 2


def test_add_task_without_description() -> None:
    """
    Test adding a task without description.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task")

    assert len(manager.tasks) == 1
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_add_task_invalid_title_empty() -> None:
    """
    Test adding a task with empty title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("")


def test_add_task_invalid_title_whitespace() -> None:
    """
    Test adding a task with whitespace-only title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("   ")


def test_list_tasks_empty() -> None:
    """
    Test listing tasks when the list is empty.
    """
    manager = TaskManager()
    tasks = manager.list_tasks()

    assert tasks == []
    assert len(tasks) == 0


def test_list_tasks_with_data() -> None:
    """
    Test listing tasks when the list has data.
    """
    manager = TaskManager()
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")

    tasks = manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

    # Verify it returns a copy, not the internal list
    original_length = len(manager.tasks)
    tasks.append(Task(id=999, title="External Task"))
    assert len(manager.tasks) == original_length  # Original should not be modified


def test_get_task_by_id_found() -> None:
    """
    Test getting a task by ID when it exists.
    """
    manager = TaskManager()
    added_task = manager.add_task("Test Task", "Description")

    retrieved_task = manager.get_task_by_id(added_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == added_task.id
    assert retrieved_task.title == added_task.title


def test_get_task_by_id_not_found() -> None:
    """
    Test getting a task by ID when it doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    retrieved_task = manager.get_task_by_id(999)
    assert retrieved_task is None


def test_update_task_valid() -> None:
    """
    Test updating an existing task.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    updated_task = manager.update_task(original_task.id, "Updated Task", "Updated Description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed == original_task.completed

    # Verify the task in the manager's list is also updated
    task_in_list = manager.get_task_by_id(original_task.id)
    assert task_in_list is not None
    assert task_in_list.title == "Updated Task"


def test_update_task_partial() -> None:
    """
    Test updating only the title of a task.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    updated_task = manager.update_task(original_task.id, title="Updated Task")

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
    manager.add_task("Test Task", "Description")

    result = manager.update_task(999, "Updated Task")
    assert result is None


def test_update_task_invalid_title() -> None:
    """
    Test updating a task with an invalid (empty) title raises ValueError.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.update_task(original_task.id, "")


def test_delete_task_exists() -> None:
    """
    Test deleting an existing task.
    """
    manager = TaskManager()
    task_to_delete = manager.add_task("Task to Delete", "Description")

    result = manager.delete_task(task_to_delete.id)
    assert result is True
    assert len(manager.tasks) == 0
    assert manager.get_task_by_id(task_to_delete.id) is None


def test_delete_task_not_exists() -> None:
    """
    Test deleting a task that doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    result = manager.delete_task(999)
    assert result is False
    assert len(manager.tasks) == 1


def test_toggle_task_completion() -> None:
    """
    Test toggling a task's completion status.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # Initially should be False
    assert task.completed is False

    # Toggle to True
    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is True

    # Toggle back to False
    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is False


def test_toggle_task_completion_not_exists() -> None:
    """
    Test toggling completion status for a task that doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    result = manager.toggle_task_completion(999)
    assert result is None


def test_id_generation_sequential() -> None:
    """
    Test that task IDs are generated sequentially.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    task3 = manager.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3
    assert manager._next_id == 4