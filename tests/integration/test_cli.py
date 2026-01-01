"""
Integration tests for CLI functionality.
"""
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch, MagicMock
from src.main import main, add_task_ui, list_tasks_ui
from src.task_manager import TaskManager


def test_add_task_ui_valid_input() -> None:
    """
    Test the add task UI with valid input.
    """
    task_manager = TaskManager()

    # Mock user input
    with patch('builtins.input', side_effect=['Test Title', 'Test Description']):
        # Capture printed output
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(task_manager)

        output = output_buffer.getvalue()
        assert "Task added successfully" in output
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0].title == "Test Title"
        assert task_manager.tasks[0].description == "Test Description"


def test_add_task_ui_empty_title() -> None:
    """
    Test the add task UI with empty title input.
    """
    task_manager = TaskManager()

    # Mock user input with empty title
    with patch('builtins.input', side_effect=['', 'Test Description']):
        # Capture printed output
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            add_task_ui(task_manager)

        output = output_buffer.getvalue()
        assert "Error: Task title cannot be empty" in output
        assert len(task_manager.tasks) == 0


def test_list_tasks_ui_empty_list() -> None:
    """
    Test the list tasks UI when the task list is empty.
    """
    task_manager = TaskManager()

    # Capture printed output
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        list_tasks_ui(task_manager)

    output = output_buffer.getvalue()
    assert "No tasks found" in output


def test_list_tasks_ui_with_tasks() -> None:
    """
    Test the list tasks UI when the task list has tasks.
    """
    task_manager = TaskManager()
    task_manager.add_task("Task 1", "Description 1")
    task_manager.add_task("Task 2", "Description 2")

    # Capture printed output
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        list_tasks_ui(task_manager)

    output = output_buffer.getvalue()
    assert "Task 1" in output
    assert "Task 2" in output
    assert "Description 1" in output
    assert "Description 2" in output


def test_list_tasks_ui_with_completed_task() -> None:
    """
    Test the list tasks UI with a completed task.
    """
    task_manager = TaskManager()
    task = task_manager.add_task("Completed Task", "Description")
    task_manager.toggle_task_completion(task.id)

    # Capture printed output
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        list_tasks_ui(task_manager)

    output = output_buffer.getvalue()
    assert "Completed Task" in output
    # Check that the completion status is shown
    assert "✓" in output or "○" in output


def test_cli_main_menu_invalid_choice() -> None:
    """
    Test the main CLI loop with an invalid menu choice.
    """
    # Mock user input: invalid choice followed by exit
    with patch('builtins.input', side_effect=['99', '6']), \
         patch('sys.argv', ['main.py']), \
         patch('src.main.TaskManager') as mock_task_manager_class:

        # Create a mock instance
        mock_task_manager = MagicMock()
        mock_task_manager.list_tasks.return_value = []
        mock_task_manager_class.return_value = mock_task_manager

        # Capture printed output
        output_buffer = io.StringIO()

        try:
            with redirect_stdout(output_buffer):
                main()
        except SystemExit:
            pass  # Expected when user chooses to exit

        output = output_buffer.getvalue()
        assert "Invalid choice" in output


def test_cli_main_menu_add_task_flow() -> None:
    """
    Test the main CLI flow for adding a task.
    """
    with patch('builtins.input', side_effect=['1', 'New Task', 'Task Description', '6']), \
         patch('sys.argv', ['main.py']), \
         patch('src.main.TaskManager') as mock_task_manager_class:

        # Create a mock instance
        mock_task_manager = MagicMock()
        mock_task_manager.add_task.return_value = MagicMock(id=1, title='New Task', description='Task Description', completed=False)
        mock_task_manager.list_tasks.return_value = []
        mock_task_manager_class.return_value = mock_task_manager

        # Capture printed output
        output_buffer = io.StringIO()

        try:
            with redirect_stdout(output_buffer):
                main()
        except SystemExit:
            pass  # Expected when user chooses to exit

        output = output_buffer.getvalue()
        # Verify that the add task functionality was triggered
        mock_task_manager.add_task.assert_called_once_with('New Task', 'Task Description')
        assert "Welcome to the Console Todo App" in output


def test_cli_main_menu_list_tasks_flow() -> None:
    """
    Test the main CLI flow for listing tasks.
    """
    with patch('builtins.input', side_effect=['2', '6']), \
         patch('sys.argv', ['main.py']), \
         patch('src.main.TaskManager') as mock_task_manager_class:

        # Create a mock instance
        mock_task_manager = MagicMock()
        mock_task_manager.list_tasks.return_value = [
            MagicMock(id=1, title='Test Task', description='Test Description', completed=False)
        ]
        mock_task_manager_class.return_value = mock_task_manager

        # Capture printed output
        output_buffer = io.StringIO()

        try:
            with redirect_stdout(output_buffer):
                main()
        except SystemExit:
            pass  # Expected when user chooses to exit

        output = output_buffer.getvalue()
        # Verify that the list tasks functionality was triggered
        mock_task_manager.list_tasks.assert_called_once()
        assert "Test Task" in output