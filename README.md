# Console Todo App

A simple command-line todo application written in Python that allows users to manage tasks in memory.

## Features

- Add tasks with title and description
- List all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- Menu-driven interface
- Input validation and error handling

## Requirements

- Python 3.13 or higher

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies (if any) using:
   ```bash
   pip install -e .
   ```
   Or with uv:
   ```bash
   uv sync
   ```

## Usage

To run the application:

```bash
cd src
python main.py
```

The application will present a menu with the following options:

1. Add task - Add a new task with title and description
2. List tasks - View all tasks with their status
3. Update task - Modify an existing task
4. Delete task - Remove a task by its ID
5. Complete task - Toggle a task's completion status
6. Exit - Quit the application

## Architecture

The application follows a clean architecture pattern:

- `src/models/task.py`: Task data model definition
- `src/task_manager.py`: Business logic and CRUD operations for tasks
- `src/main.py`: CLI interface and user interaction handling
- `tests/`: Unit and integration tests

## Running Tests

To run the tests:

```bash
# Run all tests
python -m pytest

# Run unit tests only
python -m pytest tests/unit/

# Run integration tests only
python -m pytest tests/integration/
```

## Development

This project was generated following the Spec-Driven Development (SDD) methodology with:

- A feature specification in `specs/001-console-todo-app/spec.md`
- Implementation plan in `specs/001-console-todo-app/plan.md`
- Task breakdown in `specs/001-console-todo-app/tasks.md`

## License

This project is licensed under the terms specified in the project documentation.