"""
Unit tests specifically for TaskManager list_tasks method.
"""
from src.task_manager import TaskManager


def test_list_tasks_empty() -> None:
    """
    Test listing tasks when the list is empty.
    """
    manager = TaskManager()
    tasks = manager.list_tasks()

    assert tasks == []
    assert len(tasks) == 0


def test_list_tasks_with_single_task() -> None:
    """
    Test listing tasks with a single task.
    """
    manager = TaskManager()
    added_task = manager.add_task("Test Task", "Description")

    tasks = manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == added_task.id
    assert tasks[0].title == added_task.title
    assert tasks[0].description == added_task.description
    assert tasks[0].completed == added_task.completed


def test_list_tasks_with_multiple_tasks() -> None:
    """
    Test listing tasks with multiple tasks.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    tasks = manager.list_tasks()
    assert len(tasks) == 3
    assert tasks[0].id == task1.id
    assert tasks[1].id == task2.id
    assert tasks[2].id == task3.id


def test_list_tasks_returns_copy() -> None:
    """
    Test that list_tasks returns a copy, not the internal list.
    """
    manager = TaskManager()
    manager.add_task("Task 1", "Description 1")
    manager.add_task("Task 2", "Description 2")

    original_length = len(manager.tasks)
    tasks_copy = manager.list_tasks()

    # Modify the returned list
    from src.models.task import Task
    tasks_copy.append(Task(id=999, title="External Task"))

    # The internal list should remain unchanged
    assert len(manager.tasks) == original_length
    assert len(tasks_copy) == original_length + 1


def test_list_tasks_after_modifications() -> None:
    """
    Test listing tasks after various CRUD operations.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")

    # Update a task
    manager.update_task(task1.id, "Updated Task 1")

    # Toggle completion
    manager.toggle_task_completion(task2.id)

    tasks = manager.list_tasks()
    assert len(tasks) == 2

    # Find the updated task
    updated_task = next((t for t in tasks if t.id == task1.id), None)
    assert updated_task is not None
    assert updated_task.title == "Updated Task 1"

    # Find the completed task
    completed_task = next((t for t in tasks if t.id == task2.id), None)
    assert completed_task is not None
    assert completed_task.completed is True


def test_list_tasks_after_deletion() -> None:
    """
    Test listing tasks after a task has been deleted.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")

    # Delete one task
    manager.delete_task(task1.id)

    tasks = manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == task2.id