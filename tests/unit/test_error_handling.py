"""
Unit tests for error handling in TaskManager methods.
"""
import pytest
from src.task_manager import TaskManager


def test_add_task_empty_title() -> None:
    """
    Test that adding a task with empty title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("")


def test_add_task_whitespace_only_title() -> None:
    """
    Test that adding a task with whitespace-only title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("   ")


def test_add_task_tab_only_title() -> None:
    """
    Test that adding a task with tab-only title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("\t\t")


def test_add_task_newline_only_title() -> None:
    """
    Test that adding a task with newline-only title raises ValueError.
    """
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.add_task("\n\n")


def test_update_task_empty_title() -> None:
    """
    Test that updating a task with empty title raises ValueError.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Description")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.update_task(task.id, "")


def test_update_task_whitespace_only_title() -> None:
    """
    Test that updating a task with whitespace-only title raises ValueError.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Description")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        manager.update_task(task.id, "   ")


def test_get_task_by_id_negative() -> None:
    """
    Test getting a task by negative ID returns None.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.get_task_by_id(-1)
    assert result is None


def test_get_task_by_id_zero() -> None:
    """
    Test getting a task by zero ID returns None.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.get_task_by_id(0)
    assert result is None


def test_get_task_by_id_large_number() -> None:
    """
    Test getting a task by a large non-existent ID returns None.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.get_task_by_id(999999)
    assert result is None


def test_update_task_non_existent() -> None:
    """
    Test updating a non-existent task returns None.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.update_task(999, "New Title")
    assert result is None


def test_delete_task_non_existent() -> None:
    """
    Test deleting a non-existent task returns False.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.delete_task(999)
    assert result is False


def test_toggle_task_completion_non_existent() -> None:
    """
    Test toggling completion status of a non-existent task returns None.
    """
    manager = TaskManager()
    manager.add_task("Test Task", "Description")

    result = manager.toggle_task_completion(999)
    assert result is None


def test_task_validation_empty_title() -> None:
    """
    Test Task validation with empty title.
    """
    from src.models.task import Task
    task = Task(id=1, title="Valid Title")
    task.title = ""  # Manually set to invalid state
    assert task.validate() is False


def test_task_validation_whitespace_title() -> None:
    """
    Test Task validation with whitespace-only title.
    """
    from src.models.task import Task
    task = Task(id=1, title="Valid Title")
    task.title = "   "  # Manually set to invalid state
    assert task.validate() is False


def test_task_validation_negative_id() -> None:
    """
    Test Task validation with negative ID.
    """
    from src.models.task import Task
    task = Task(id=1, title="Valid Title")
    task.id = -1  # Manually set to invalid state
    assert task.validate() is False


def test_task_validation_zero_id() -> None:
    """
    Test Task validation with zero ID.
    """
    from src.models.task import Task
    task = Task(id=1, title="Valid Title")
    task.id = 0  # Manually set to invalid state
    assert task.validate() is False


def test_task_validation_non_boolean_completed() -> None:
    """
    Test Task validation with non-boolean completed status.
    """
    from src.models.task import Task
    task = Task(id=1, title="Valid Title")
    task.completed = "not_a_boolean"  # type: ignore
    assert task.validate() is False


def test_task_post_init_empty_title() -> None:
    """
    Test Task __post_init__ validation with empty title raises ValueError.
    """
    from src.models.task import Task
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(id=1, title="")


def test_task_post_init_whitespace_title() -> None:
    """
    Test Task __post_init__ validation with whitespace-only title raises ValueError.
    """
    from src.models.task import Task
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(id=1, title="   ")


def test_task_post_init_negative_id() -> None:
    """
    Test Task __post_init__ validation with negative ID raises ValueError.
    """
    from src.models.task import Task
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=-1, title="Valid Title")


def test_task_post_init_zero_id() -> None:
    """
    Test Task __post_init__ validation with zero ID raises ValueError.
    """
    from src.models.task import Task
    with pytest.raises(ValueError, match="Task ID must be a positive integer"):
        Task(id=0, title="Valid Title")


def test_update_task_with_none_values() -> None:
    """
    Test updating a task with None values doesn't trigger validation errors.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # This should not raise any validation errors
    result = manager.update_task(task.id, None, None)
    assert result is not None
    assert result.title == "Original Task"
    assert result.description == "Original Description"


def test_update_task_partial_with_none_and_valid() -> None:
    """
    Test updating a task with a mix of None and valid values.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # Update only description, leave title as None (no change)
    result = manager.update_task(task.id, None, "New Description")
    assert result is not None
    assert result.title == "Original Task"
    assert result.description == "New Description"


def test_multiple_validation_errors_sequentially() -> None:
    """
    Test multiple validation errors can occur sequentially without affecting the manager state.
    """
    manager = TaskManager()
    initial_task_count = len(manager.tasks)

    # Try to add tasks with invalid titles multiple times
    for _ in range(3):
        try:
            manager.add_task("")
        except ValueError:
            pass  # Expected

    # The task count should remain unchanged
    assert len(manager.tasks) == initial_task_count

    # Add a valid task to ensure manager still works
    valid_task = manager.add_task("Valid Task", "Description")
    assert valid_task is not None
    assert len(manager.tasks) == initial_task_count + 1