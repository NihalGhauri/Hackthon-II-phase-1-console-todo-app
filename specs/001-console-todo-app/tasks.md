---
description: "Task list for console todo app implementation"
---

# Tasks: Console Todo App

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/, tests/, pyproject.toml
- [x] T002 [P] Initialize Python project with pyproject.toml dependencies
- [x] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task model with type hints in src/models/task.py
- [x] T005 [P] Create TaskManager class with CRUD operations in src/task_manager.py
- [x] T006 [P] Setup basic CLI structure in src/main.py
- [x] T007 Create error handling and validation utilities
- [x] T008 Configure environment and configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks to their todo list and view them in a clean format

**Independent Test**: Can be fully tested by starting the app, adding a task, listing tasks, and verifying the task appears in the list with correct details.

### Tests for User Story 1 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [x] T010 [P] [US1] Unit test for TaskManager add_task method in tests/unit/test_task_manager.py
- [x] T011 [P] [US1] Unit test for TaskManager list_tasks method in tests/unit/test_task_manager.py
- [x] T012 [US1] Integration test for CLI add/list functionality in tests/integration/test_cli.py

### Implementation for User Story 1

- [x] T013 [P] [US1] Implement Task model with validation in src/models/task.py
- [x] T014 [US1] Implement add_task method in src/task_manager.py
- [x] T015 [US1] Implement list_tasks method in src/task_manager.py
- [x] T016 [US1] Implement CLI add task functionality in src/main.py
- [x] T017 [US1] Implement CLI list tasks functionality in src/main.py
- [x] T018 [US1] Add input validation for add task in src/main.py
- [x] T019 [US1] Add output formatting for list tasks in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Allow users to modify or remove tasks they've previously added

**Independent Test**: Can be fully tested by adding tasks, updating a task by ID, verifying changes, then deleting a task by ID and confirming it's removed.

### Tests for User Story 2 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T020 [P] [US2] Unit test for TaskManager update_task method in tests/unit/test_task_manager_update.py
- [x] T021 [P] [US2] Unit test for TaskManager delete_task method in tests/unit/test_task_manager_delete.py
- [x] T022 [US2] Integration test for CLI update/delete functionality in tests/integration/test_cli_update_delete.py

### Implementation for User Story 2

- [x] T023 [US2] Implement update_task method in src/task_manager.py
- [x] T024 [US2] Implement delete_task method in src/task_manager.py
- [x] T025 [US2] Implement CLI update task functionality in src/main.py
- [x] T026 [US2] Implement CLI delete task functionality in src/main.py
- [x] T027 [US2] Add input validation for update/delete in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P3)

**Goal**: Allow users to track the completion status of their tasks

**Independent Test**: Can be fully tested by adding tasks, marking a task as complete, verifying the status change, then toggling it back to incomplete.

### Tests for User Story 3 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T028 [P] [US3] Unit test for TaskManager toggle_task_completion method in tests/unit/test_task_manager_toggle.py
- [x] T029 [US3] Integration test for CLI complete functionality in tests/integration/test_cli_complete.py

### Implementation for User Story 3

- [x] T030 [US3] Implement toggle_task_completion method in src/task_manager.py
- [x] T031 [US3] Implement CLI complete task functionality in src/main.py
- [x] T032 [US3] Add input validation for complete task in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Error Handling & Edge Cases (Priority: P4)

**Goal**: Handle invalid inputs gracefully and implement proper error handling

**Independent Test**: Can be tested by providing invalid inputs and verifying helpful error messages without crashes.

### Tests for Error Handling (TDD approach) ⚠️

- [x] T033 [P] [US4] Unit test for error handling in TaskManager methods in tests/unit/test_error_handling.py
- [x] T034 [US4] Integration test for CLI error handling in tests/integration/test_cli_error_handling.py

### Implementation for Error Handling

- [x] T035 [US4] Implement validation for empty task title in src/task_manager.py
- [x] T036 [US4] Implement validation for invalid task IDs in src/task_manager.py
- [x] T037 [US4] Implement validation for empty task list in src/task_manager.py
- [x] T038 [US4] Add user-friendly error messages in src/main.py
- [x] T039 [US4] Implement graceful handling of invalid menu selections in src/main.py

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T040 [P] Documentation updates in README.md
- [x] T041 Code cleanup and refactoring
- [x] T042 Performance optimization for all operations
- [x] T043 [P] Additional unit tests in tests/unit/
- [x] T044 Security hardening
- [x] T045 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Affects all other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Unit test for TaskManager add_task method in tests/unit/test_task_manager.py"
Task: "Unit test for TaskManager list_tasks method in tests/unit/test_task_manager.py"
Task: "Integration test for CLI add/list functionality in tests/integration/test_cli.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement Task model with validation in src/models/task.py"
Task: "Implement add_task method in src/task_manager.py"
Task: "Implement list_tasks method in src/task_manager.py"
Task: "Implement CLI add task functionality in src/main.py"
Task: "Implement CLI list tasks functionality in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence