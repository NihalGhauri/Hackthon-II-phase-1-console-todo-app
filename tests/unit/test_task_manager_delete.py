"""
Unit tests specifically for TaskManager delete_task method.
"""
import pytest
from src.task_manager import TaskManager


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
    assert len(manager.tasks) == 1  # Should remain unchanged


def test_delete_task_from_multiple() -> None:
    """
    Test deleting one task from multiple tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete the middle task
    result = manager.delete_task(task2.id)
    assert result is True
    assert len(manager.tasks) == 2

    # Verify remaining tasks are still there
    assert manager.get_task_by_id(task1.id) is not None
    assert manager.get_task_by_id(task2.id) is None  # Should be deleted
    assert manager.get_task_by_id(task3.id) is not None


def test_delete_first_task() -> None:
    """
    Test deleting the first task in the list.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete the first task
    result = manager.delete_task(task1.id)
    assert result is True
    assert len(manager.tasks) == 2

    # Verify task2 and task3 are still there
    remaining_tasks = manager.list_tasks()
    assert len(remaining_tasks) == 2
    assert all(t.id != task1.id for t in remaining_tasks)


def test_delete_last_task() -> None:
    """
    Test deleting the last task in the list.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete the last task
    result = manager.delete_task(task3.id)
    assert result is True
    assert len(manager.tasks) == 2

    # Verify task1 and task2 are still there
    remaining_tasks = manager.list_tasks()
    assert len(remaining_tasks) == 2
    assert all(t.id != task3.id for t in remaining_tasks)


def test_delete_only_task() -> None:
    """
    Test deleting the only task in the list.
    """
    manager = TaskManager()
    task = manager.add_task("Only Task", "Description")

    result = manager.delete_task(task.id)
    assert result is True
    assert len(manager.tasks) == 0

    # Verify the list is now empty
    assert manager.list_tasks() == []


def test_delete_task_preserves_ids() -> None:
    """
    Test that deleting a task doesn't affect the IDs of other tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete task2
    manager.delete_task(task2.id)

    # Verify that task1 and task3 still have their original IDs
    remaining_task1 = manager.get_task_by_id(task1.id)
    remaining_task3 = manager.get_task_by_id(task3.id)
    assert remaining_task1 is not None
    assert remaining_task1.id == task1.id
    assert remaining_task3 is not None
    assert remaining_task3.id == task3.id


def test_delete_task_with_completed_status() -> None:
    """
    Test deleting a task that has been marked as completed.
    """
    manager = TaskManager()
    task = manager.add_task("Completed Task", "Description")
    manager.toggle_task_completion(task.id)  # Mark as completed

    # Verify it's completed before deletion
    task_in_manager = manager.get_task_by_id(task.id)
    assert task_in_manager is not None
    assert task_in_manager.completed is True

    # Delete the task
    result = manager.delete_task(task.id)
    assert result is True
    assert manager.get_task_by_id(task.id) is None


def test_delete_task_does_not_affect_next_id() -> None:
    """
    Test that deleting a task doesn't affect the next ID generation.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    next_id_before = manager.get_next_id()

    # Delete task1
    manager.delete_task(task1.id)
    next_id_after = manager.get_next_id()

    # The next_id should remain the same
    assert next_id_before == next_id_after

    # Adding a new task should get the next sequential ID
    new_task = manager.add_task("New Task", "Description")
    assert new_task.id == next_id_before


def test_delete_all_tasks() -> None:
    """
    Test deleting all tasks one by one.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete all tasks
    assert manager.delete_task(task1.id) is True
    assert manager.delete_task(task2.id) is True
    assert manager.delete_task(task3.id) is True

    # Verify the list is empty
    assert len(manager.tasks) == 0
    assert manager.list_tasks() == []