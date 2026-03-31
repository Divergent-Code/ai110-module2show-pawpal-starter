# PawPal Refactoring Plan

The recent introduction of the `core/` package split the monolithic `pawpal_system.py` into distinct components (`task.py`, `pet.py`, `owner.py`, `scheduler.py`). However, the existing code and files were disjointed during the process.

## User Review Required

> [!WARNING]
> Please review this plan. Approving it will delete duplicated legacy logic and enforce the new package structure.

## Proposed Changes

### Core Package Refactoring

I will point all remaining code to the new `core/` directory and safely eliminate the old `pawpal_system.py` to prevent duplicate source code maintenance.

#### [MODIFY] [main.py](file:///c:/Users/onika/OneDrive/Documents/Coding%20Projects/CodePath%20Projects/ai110-module2show-pawpal-starter/main.py)

- Change import from `pawpal_system` to `core`.
- Update the way it fetches the schedule, since `Scheduler.get_sorted_schedule()` was removed in both old and new versions. We will update `main.py` to instead call `brain.get_all_tasks()` and then `brain.sort_by_time(tasks)`.

#### [DELETE] [pawpal_system.py](file:///c:/Users/onika/OneDrive/Documents/Coding%20Projects/CodePath%20Projects/ai110-module2show-pawpal-starter/pawpal_system.py)

- This file contains identical classes (`Task`, `Pet`, `Owner`, `Scheduler`) to the ones in `core/`. Deleting it ensures there is a single source of truth for the project.

## Open Questions

> [!IMPORTANT]
>
> 1. You recently deleted `tests/test_paypal.py`. Would you like me to recreate the test file under `tests/test_pawpal.py` pointed properly to the new `core` module?
> 2. You also deleted `app.py` (the Streamlit UI starter file). Should I leave it deleted, or recreate it using your new engine?

## Verification Plan

### Automated Tests

- Run `python main.py` to verify it successfully builds the CLI schedule and prints without throwing an `AttributeError`.
- (If agreed) Run pytest again on the recreated test suite.
