"""
Unit tests specifically for TaskManager toggle_task_completion method.
"""
import pytest
from src.task_manager import TaskManager


def test_toggle_task_completion_from_false_to_true() -> None:
    """
    Test toggling a task's completion status from False to True.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # Initially should be False
    assert task.completed is False

    # Toggle to True
    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is True

    # Verify in the manager too
    task_in_manager = manager.get_task_by_id(task.id)
    assert task_in_manager is not None
    assert task_in_manager.completed is True


def test_toggle_task_completion_from_true_to_false() -> None:
    """
    Test toggling a task's completion status from True to False.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # First toggle to True
    manager.toggle_task_completion(task.id)
    task_in_manager = manager.get_task_by_id(task.id)
    assert task_in_manager is not None
    assert task_in_manager.completed is True

    # Then toggle back to False
    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is False

    # Verify in the manager too
    task_in_manager = manager.get_task_by_id(task.id)
    assert task_in_manager is not None
    assert task_in_manager.completed is False


def test_toggle_task_completion_not_found() -> None:
    """
    Test toggling completion status for a task that doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    result = manager.toggle_task_completion(999)
    assert result is None


def test_toggle_multiple_tasks() -> None:
    """
    Test toggling completion status for multiple tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Toggle task2 to True
    toggled_task = manager.toggle_task_completion(task2.id)
    assert toggled_task is not None
    assert toggled_task.completed is True

    # Verify other tasks remain unchanged
    task1_in_manager = manager.get_task_by_id(task1.id)
    task3_in_manager = manager.get_task_by_id(task3.id)
    assert task1_in_manager is not None
    assert task1_in_manager.completed is False
    assert task3_in_manager is not None
    assert task3_in_manager.completed is False

    # Toggle task1 to True
    manager.toggle_task_completion(task1.id)
    task1_in_manager = manager.get_task_by_id(task1.id)
    task2_in_manager = manager.get_task_by_id(task2.id)
    assert task1_in_manager is not None
    assert task1_in_manager.completed is True
    assert task2_in_manager is not None
    assert task2_in_manager.completed is True
    assert task3_in_manager is not None
    assert task3_in_manager.completed is False


def test_toggle_all_tasks() -> None:
    """
    Test toggling completion status for all tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Toggle all to True
    manager.toggle_task_completion(task1.id)
    manager.toggle_task_completion(task2.id)
    manager.toggle_task_completion(task3.id)

    task1_in_manager = manager.get_task_by_id(task1.id)
    task2_in_manager = manager.get_task_by_id(task2.id)
    task3_in_manager = manager.get_task_by_id(task3.id)

    assert task1_in_manager is not None and task1_in_manager.completed is True
    assert task2_in_manager is not None and task2_in_manager.completed is True
    assert task3_in_manager is not None and task3_in_manager.completed is True

    # Toggle all back to False
    manager.toggle_task_completion(task1.id)
    manager.toggle_task_completion(task2.id)
    manager.toggle_task_completion(task3.id)

    task1_in_manager = manager.get_task_by_id(task1.id)
    task2_in_manager = manager.get_task_by_id(task2.id)
    task3_in_manager = manager.get_task_by_id(task3.id)

    assert task1_in_manager is not None and task1_in_manager.completed is False
    assert task2_in_manager is not None and task2_in_manager.completed is False
    assert task3_in_manager is not None and task3_in_manager.completed is False


def test_toggle_completion_preserves_other_attributes() -> None:
    """
    Test that toggling completion status preserves other task attributes.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Title", "Original Description")

    # Store the original completion status before toggle
    original_completed_status = original_task.completed
    # Initially the task should be incomplete
    assert original_completed_status is False

    # Toggle completion
    toggled_task = manager.toggle_task_completion(original_task.id)

    assert toggled_task is not None
    assert toggled_task.id == original_task.id
    assert toggled_task.title == original_task.title
    assert toggled_task.description == original_task.description
    # The completion status should be the only thing that changed
    assert toggled_task.completed is True  # Should now be completed
    assert toggled_task.completed != original_completed_status  # Different from initial state


def test_toggle_completion_with_empty_description() -> None:
    """
    Test toggling completion status for a task with empty description.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task")  # No description provided

    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is True
    assert toggled_task.description == ""


def test_toggle_completion_multiple_times() -> None:
    """
    Test toggling completion status multiple times on the same task.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # Toggle 5 times: F->T->F->T->F
    expected_states = [True, False, True, False]
    for expected_state in expected_states:
        toggled_task = manager.toggle_task_completion(task.id)
        assert toggled_task is not None
        assert toggled_task.completed is expected_state


def test_toggle_completion_on_task_with_special_characters() -> None:
    """
    Test toggling completion status on a task with special characters in title/description.
    """
    manager = TaskManager()
    task = manager.add_task("Task with @#$%", "Description with üñíçødé")

    toggled_task = manager.toggle_task_completion(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is True
    assert toggled_task.title == "Task with @#$%"
    assert toggled_task.description == "Description with üñíçødé"


def test_toggle_completion_on_large_task_list() -> None:
    """
    Test toggling completion status on a task in a large list.
    """
    manager = TaskManager()

    # Add 100 tasks
    tasks = []
    for i in range(100):
        task = manager.add_task(f"Task {i}", f"Description {i}")
        tasks.append(task)

    # Toggle a task in the middle
    middle_task = tasks[50]
    toggled_task = manager.toggle_task_completion(middle_task.id)

    assert toggled_task is not None
    assert toggled_task.completed is True

    # Verify other tasks are not affected
    first_task = manager.get_task_by_id(tasks[0].id)
    last_task = manager.get_task_by_id(tasks[99].id)
    assert first_task is not None and first_task.completed is False
    assert last_task is not None and last_task.completed is False