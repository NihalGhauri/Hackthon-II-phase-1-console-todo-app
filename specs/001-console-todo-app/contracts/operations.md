# API Contracts: Console Todo App

## Task Management Operations

### Add Task
**Endpoint**: CLI command `add`
**Input**:
- title (string, required)
- description (string, optional)

**Output**:
- Success: Task object with assigned ID
- Error: Error message

**Validation**:
- Title must not be empty
- Description can be empty

### List Tasks
**Endpoint**: CLI command `list`
**Input**: None
**Output**:
- Array of Task objects with all fields

### Update Task
**Endpoint**: CLI command `update`
**Input**:
- id (integer, required)
- title (string, optional)
- description (string, optional)

**Output**:
- Success: Updated Task object
- Error: Error message

**Validation**:
- Task with given ID must exist
- At least one field to update must be provided

### Delete Task
**Endpoint**: CLI command `delete`
**Input**:
- id (integer, required)

**Output**:
- Success: Confirmation message
- Error: Error message

**Validation**:
- Task with given ID must exist

### Toggle Task Completion
**Endpoint**: CLI command `complete`
**Input**:
- id (integer, required)

**Output**:
- Success: Updated Task object with toggled completion status
- Error: Error message

**Validation**:
- Task with given ID must exist