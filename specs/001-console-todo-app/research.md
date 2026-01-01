# Research: Console Todo App

## Decision: Architecture Pattern
**Rationale**: Chose a clean architecture pattern with separation of concerns to ensure maintainability and testability. The design separates data models, business logic (TaskManager), and presentation (CLI interface).
**Alternatives considered**:
- Monolithic approach (single file): Discarded due to maintainability concerns
- MVC pattern: Considered but overkill for this simple application

## Decision: Data Storage
**Rationale**: Using Python list of dictionaries for in-memory storage as specified in requirements. This meets the "session-only persistence" requirement without adding complexity of external storage.
**Alternatives considered**:
- Python classes with instance variables: More complex for simple storage needs
- External file storage: Contradicts requirement for in-memory only

## Decision: Task ID Generation
**Rationale**: Implement auto-incrementing integer IDs starting from 1 using a class variable in TaskManager to ensure uniqueness across all tasks in the session.
**Alternatives considered**:
- UUID generation: Overkill for session-only, human-unfriendly
- Random integers: Risk of collisions

## Decision: Error Handling
**Rationale**: Implement comprehensive input validation and exception handling with user-friendly error messages to meet requirement for graceful handling of invalid inputs.
**Alternatives considered**:
- Minimal error handling: Would not meet specification requirements
- Generic exception handling: Would not provide helpful feedback to users

## Decision: CLI Interface Design
**Rationale**: Menu-driven interface with numbered options provides clear user experience and matches common console application patterns.
**Alternatives considered**:
- Command-line arguments: Less user-friendly for interactive use
- Natural language processing: Overly complex for specified requirements