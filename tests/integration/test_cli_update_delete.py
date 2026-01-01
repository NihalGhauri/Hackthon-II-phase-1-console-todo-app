"""
Integration tests specifically for CLI update/delete functionality.
"""
import io
import sys
from contextlib import redirect_stdout
from unittest.mock import patch
from src.main import update_task_ui, delete_task_ui
from src.task_manager import TaskManager


def test_update_task_ui_valid_input() -> None:
    """
    Test the update task UI with valid input.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # Mock user input: task ID, new title, new description
    with patch('builtins.input', side_effect=[str(task.id), "Updated Task", "Updated Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        assert "Task 1 updated successfully" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"


def test_update_task_ui_partial_update_title() -> None:
    """
    Test the update task UI updating only the title.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # Mock user input: task ID, new title, press Enter to keep description
    with patch('builtins.input', side_effect=[str(task.id), "Updated Task", ""]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        assert "Task 1 updated successfully" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Original Description"  # Should remain unchanged


def test_update_task_ui_partial_update_description() -> None:
    """
    Test the update task UI updating only the description.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # Mock user input: task ID, press Enter to keep title, new description
    with patch('builtins.input', side_effect=[str(task.id), "", "Updated Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        assert "Task 1 updated successfully" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.title == "Original Task"  # Should remain unchanged
        assert updated_task.description == "Updated Description"


def test_update_task_ui_task_not_found() -> None:
    """
    Test the update task UI when the task doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: non-existent task ID
    with patch('builtins.input', side_effect=["999", "New Title", "New Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        assert "not found" in output
        assert len(manager.tasks) == 1  # No changes should be made


def test_update_task_ui_invalid_task_id() -> None:
    """
    Test the update task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: invalid task ID (non-numeric)
    with patch('builtins.input', side_effect=["invalid", "New Title", "New Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function
        # which should handle the ValueError from int conversion


def test_update_task_ui_empty_title() -> None:
    """
    Test the update task UI with an empty title.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # Mock user input: task ID, empty title
    with patch('builtins.input', side_effect=[str(task.id), "", "Updated Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        # The update should work since we're only updating the description


def test_delete_task_ui_valid_input() -> None:
    """
    Test the delete task UI with valid input.
    """
    manager = TaskManager()
    task = manager.add_task("Task to Delete", "Description")

    # Mock user input: task ID
    with patch('builtins.input', side_effect=[str(task.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task.id} deleted successfully" in output
        assert len(manager.tasks) == 0


def test_delete_task_ui_task_not_found() -> None:
    """
    Test the delete task UI when the task doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: non-existent task ID
    with patch('builtins.input', side_effect=["999"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        assert "not found" in output
        assert len(manager.tasks) == 1  # No changes should be made


def test_delete_task_ui_invalid_task_id() -> None:
    """
    Test the delete task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: invalid task ID (non-numeric)
    with patch('builtins.input', side_effect=["invalid"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function


def test_delete_task_ui_multiple_tasks() -> None:
    """
    Test the delete task UI with multiple tasks in the list.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Delete task2
    with patch('builtins.input', side_effect=[str(task2.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task2.id} deleted successfully" in output
        assert len(manager.tasks) == 2

        # Verify other tasks remain
        assert manager.get_task_by_id(task1.id) is not None
        assert manager.get_task_by_id(task2.id) is None
        assert manager.get_task_by_id(task3.id) is not None


def test_update_and_delete_combined_flow() -> None:
    """
    Test a combined flow of updating and then deleting a task via CLI.
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Original Description")

    # First update the task
    with patch('builtins.input', side_effect=[str(task.id), "Updated Task", "Updated Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        assert "updated successfully" in output

    # Verify the update worked
    updated_task = manager.get_task_by_id(task.id)
    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"

    # Then delete the task
    with patch('builtins.input', side_effect=[str(task.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        assert "deleted successfully" in output

    # Verify the task is gone
    assert len(manager.tasks) == 0
    assert manager.get_task_by_id(task.id) is None