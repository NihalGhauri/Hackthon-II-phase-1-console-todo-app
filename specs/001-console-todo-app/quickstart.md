# Quickstart: Console Todo App

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Navigate to project directory
3. Install dependencies: `uv sync` (or `pip install -r requirements.txt`)

## Running the Application
```bash
cd src
python main.py
```

## Basic Usage
1. The application starts with a menu of options
2. Select an option by entering the corresponding number
3. Follow the prompts to enter required information
4. View results or error messages

## Example Workflow
1. Start the app: `python main.py`
2. Select "Add task" option
3. Enter task title and description
4. Select "List tasks" to view all tasks
5. Select "Complete task" to mark a task as done
6. Select "Exit" when finished

## Common Operations
- **Add task**: Creates a new task with auto-generated ID
- **List tasks**: Shows all tasks with ID, title, description, and status
- **Update task**: Modify existing task details
- **Delete task**: Remove a task by ID
- **Complete task**: Toggle completion status for a task
- **Exit**: Quit the application