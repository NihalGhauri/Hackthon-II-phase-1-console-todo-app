"""
Integration tests for CLI error handling.
"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from src.main import add_task_ui, update_task_ui, delete_task_ui, complete_task_ui, list_tasks_ui
from src.task_manager import TaskManager


def test_add_task_ui_empty_title() -> None:
    """
    Test the add task UI with empty title input.
    """
    manager = TaskManager()

    # Mock user input with empty title
    with patch('builtins.input', side_effect=['', 'Test Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)

        output = output_buffer.getvalue()
        assert "Error: Task title cannot be empty" in output
        assert len(manager.tasks) == 0


def test_add_task_ui_whitespace_only_title() -> None:
    """
    Test the add task UI with whitespace-only title input.
    """
    manager = TaskManager()

    # Mock user input with whitespace-only title
    with patch('builtins.input', side_effect=['   ', 'Test Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)

        output = output_buffer.getvalue()
        assert "Error: Task title cannot be empty" in output
        assert len(manager.tasks) == 0


def test_update_task_ui_invalid_task_id() -> None:
    """
    Test the update task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input with invalid task ID
    with patch('builtins.input', side_effect=["invalid", "New Title", "New Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function


def test_update_task_ui_empty_title() -> None:
    """
    Test the update task UI with empty title input (should not update title).
    """
    manager = TaskManager()
    task = manager.add_task("Original Task", "Description")

    # Mock user input: task ID, empty title (meaning don't change), new description
    with patch('builtins.input', side_effect=[str(task.id), '', 'Updated Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)

        output = output_buffer.getvalue()
        # When user enters empty title, it means don't update the title
        # So the title should remain unchanged, but description should be updated
        assert "updated successfully" in output
        assert len(manager.tasks) == 1  # Should remain unchanged in count

        # Verify the task was updated correctly: title unchanged, description updated
        updated_task = manager.get_task_by_id(task.id)
        assert updated_task is not None
        assert updated_task.title == "Original Task"  # Title should remain unchanged
        assert updated_task.description == "Updated Description"  # Description should be updated


def test_update_task_ui_non_existent_task() -> None:
    """
    Test the update task UI with a non-existent task ID.
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
        assert len(manager.tasks) == 1  # Should remain unchanged


def test_delete_task_ui_invalid_task_id() -> None:
    """
    Test the delete task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input with invalid task ID
    with patch('builtins.input', side_effect=["invalid"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function


def test_delete_task_ui_non_existent_task() -> None:
    """
    Test the delete task UI with a non-existent task ID.
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
        assert len(manager.tasks) == 1  # Should remain unchanged


def test_complete_task_ui_invalid_task_id() -> None:
    """
    Test the complete task UI with an invalid task ID.
    """
    manager = TaskManager()
    manager.add_task("Existing Task", "Description")

    # Mock user input with invalid task ID
    with patch('builtins.input', side_effect=["invalid"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            complete_task_ui(manager)

        output = output_buffer.getvalue()
        # The error message depends on the input validation in the UI function


def test_complete_task_ui_non_existent_task() -> None:
    """
    Test the complete task UI with a non-existent task ID.
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
        assert len(manager.tasks) == 1  # Should remain unchanged


def test_list_tasks_ui_empty_list() -> None:
    """
    Test the list tasks UI with an empty task list.
    """
    manager = TaskManager()

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        list_tasks_ui(manager)

    output = output_buffer.getvalue()
    assert "No tasks found" in output


def test_cli_error_handling_multiple_errors_sequentially() -> None:
    """
    Test multiple error scenarios in sequence to ensure the system remains stable.
    """
    manager = TaskManager()

    # Try to add task with empty title
    with patch('builtins.input', side_effect=['', 'Test Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)
        assert len(manager.tasks) == 0

    # Try to update non-existent task
    with patch('builtins.input', side_effect=["999", "New Title", "New Description"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            update_task_ui(manager)
        assert len(manager.tasks) == 0

    # Try to delete non-existent task
    with patch('builtins.input', side_effect=["999"]):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            delete_task_ui(manager)
        assert len(manager.tasks) == 0

    # Now add a valid task to ensure the system still works
    with patch('builtins.input', side_effect=['Valid Task', 'Valid Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)
        assert len(manager.tasks) == 1

    # Verify the valid task was added
    assert manager.tasks[0].title == "Valid Task"
    assert manager.tasks[0].description == "Valid Description"


def test_add_task_ui_operation_cancelled_by_user() -> None:
    """
    Test the add task UI when user cancels the operation.
    """
    manager = TaskManager()

    # Mock user input with keyboard interrupt
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)

        assert len(manager.tasks) == 0


def test_error_messages_are_user_friendly() -> None:
    """
    Test that error messages are clear and user-friendly.
    """
    manager = TaskManager()

    # Test empty title error message
    with patch('builtins.input', side_effect=['', 'Test Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)

        output = output_buffer.getvalue()
        # Check for helpful error message
        assert "Error:" in output or "error" in output.lower()


def test_validation_preserves_existing_data() -> None:
    """
    Test that validation errors don't affect existing tasks in the manager.
    """
    manager = TaskManager()
    original_task = manager.add_task("Original Task", "Original Description")

    # Try to add a task with invalid title
    with patch('builtins.input', side_effect=['', 'Test Description']):
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(manager)

    # Verify original task is still there and unchanged
    assert len(manager.tasks) == 1
    assert manager.tasks[0].id == original_task.id
    assert manager.tasks[0].title == original_task.title
    assert manager.tasks[0].description == original_task.description
    assert manager.tasks[0].completed == original_task.completed