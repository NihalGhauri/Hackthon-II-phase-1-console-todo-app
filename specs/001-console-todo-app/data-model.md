# Data Model: Console Todo App

## Entities

### Task
**Description**: Represents a single todo item in the application

**Fields**:
- `id`: Integer - Unique identifier (auto-incrementing, starts from 1)
- `title`: String - Short description of the task (required)
- `description`: String - Detailed explanation of the task (optional, can be empty string)
- `completed`: Boolean - Completion status (default: False)

**Validation Rules**:
- `id` must be a positive integer
- `title` must not be empty or contain only whitespace
- `completed` must be a boolean value

**State Transitions**:
- `incomplete` → `complete`: When user marks task as complete
- `complete` → `incomplete`: When user marks completed task as incomplete

## Collections

### Task List
**Description**: In-memory collection of Task entities

**Operations**:
- Add: Insert new Task with auto-generated ID
- Read: Retrieve Task by ID or list all Tasks
- Update: Modify Task properties by ID
- Delete: Remove Task by ID

**Constraints**:
- IDs must be unique within the collection
- IDs must be sequential starting from 1
- Collection exists only for the duration of the session