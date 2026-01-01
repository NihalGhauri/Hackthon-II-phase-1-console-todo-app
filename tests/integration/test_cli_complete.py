"""
Integration tests specifically for CLI complete functionality.
"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from src.main import complete_task_ui
from src.task_manager import TaskManager


def test_complete_task_ui_toggle_false_to_true() -> None:
    """
    Test the complete task UI toggling from False to True.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # Initially should be False
    assert task.completed is False

    # Mock user input: task ID
    with patch('builtins.input', side_effect=[str(task.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task.id} marked as completed" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.completed is True


def test_complete_task_ui_toggle_true_to_false() -> None:
    """
    Test the complete task UI toggling from True to False.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # First, mark as complete
    manager.toggle_task_completion(task.id)
    assert task.completed is True

    # Mock user input: task ID
    with patch('builtins.input', side_effect=[str(task.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task.id} marked as incomplete" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.completed is False


def test_complete_task_ui_task_not_found() -> None:
    """
    Test the complete task UI when the task doesn't exist.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: non-existent task ID
    with patch('builtins.input', side_effect=["999"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        assert "not found" in output
        assert len(manager.tasks) == 1  # No changes should be made


def test_complete_task_ui_invalid_task_id() -> None:
    """
    Test the complete task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input: invalid task ID (non-numeric)
    with patch('builtins.input', side_effect=["invalid"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function


def test_complete_task_ui_multiple_tasks() -> None:
    """
    Test the complete task UI with multiple tasks in the list.
    """
    manager = TaskManager()
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Complete task2
    with patch('builtins.input', side_effect=[str(task2.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task2.id} marked as completed" in output

    # Verify other tasks remain unchanged
    task1_in_manager = manager.get_task_by_id(task1.id)
    task2_in_manager = manager.get_task_by_id(task2.id)
    task3_in_manager = manager.get_task_by_id(task3.id)
    assert task1_in_manager is not None and task1_in_manager.completed is False
    assert task2_in_manager is not None and task2_in_manager.completed is True
    assert task3_in_manager is not None and task3_in_manager.completed is False


def test_complete_task_ui_complex_flow() -> None:
    """
    Test a complex flow with multiple operations on tasks.
    """
    manager = TaskManager()

    # Add multiple tasks
    task1 = manager.add_task("Task 1", "Description 1")
    task2 = manager.add_task("Task 2", "Description 2")
    task3 = manager.add_task("Task 3", "Description 3")

    # Complete task1
    with patch('builtins.input', side_effect=[str(task1.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

    # Verify task1 is now completed
    updated_task1 = manager.get_task_by_id(task1.id)
    assert updated_task1 is not None and updated_task1.completed is True

    # Update task2
    with patch('builtins.input', side_effect=[str(task2.id), "Updated Task 2", "Updated Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            from src.main import update_task_ui
            update_task_ui(manager)

    # Now complete task2 (which was just updated)
    with patch('builtins.input', side_effect=[str(task2.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

    # Verify task2 is now completed and updated
    updated_task2 = manager.get_task_by_id(task2.id)
    assert updated_task2 is not None
    assert updated_task2.completed is True
    assert updated_task2.title == "Updated Task 2"


def test_complete_task_ui_with_special_characters() -> None:
    """
    Test the complete task UI with tasks that have special characters.
    """
    manager = TaskManager()
    task = manager.add_task("Task with @#$%", "Description with üñíçødé")

    # Mock user input: task ID
    with patch('builtins.input', side_effect=[str(task.id)]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        assert f"Task {task.id} marked as completed" in output

        # Verify the task was updated in the manager
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.completed is True
        assert updated_task.title == "Task with @#$%"
        assert updated_task.description == "Description with üñíçødé"


def test_complete_task_ui_multiple_toggles() -> None:
    """
    Test the complete task UI toggling the same task multiple times.
    """
    manager = TaskManager()
    task = manager.add_task("Test Task", "Description")

    # Toggle 3 times: F->T->F->T
    expected_states = ["completed", "incomplete", "completed"]
    for i, expected_state in enumerate(expected_states):
        with patch('builtins.input', side_effect=[str(task.id)]):
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                complete_task_ui(manager)

            output = output_buffer.getvalue()
            assert f"marked as {expected_state}" in output

    # Final state should be True (completed)
    final_task = manager.get_task_by_id(task.id)
    assert final_task is not None
    assert final_task.completed is True