import pytest
from datetime import datetime, timedelta
from core import Owner, Pet, Task, Scheduler

def test_sorting_correctness():
    """Verify the Brain correctly sorts tasks chronologically."""
    me = Owner("Test Owner")
    dog = Pet("Test Dog", "Dog")
    me.add_pet(dog)
    
    # Add tasks out of order
    dog.add_task(Task("Evening Feed", "18:00", "Daily", "Medium"))
    dog.add_task(Task("Morning Walk", "08:00", "Daily", "High"))
    
    brain = Scheduler(me)
    all_tasks = brain.get_all_tasks()
    sorted_tasks = brain.sort_by_time(all_tasks)
    
    # Assert that the first task in the list is the Morning Walk
    assert sorted_tasks[0].description == "Morning Walk"
    assert sorted_tasks[1].description == "Evening Feed"

def test_conflict_detection():
    """Verify the Brain catches identically timed tasks."""
    me = Owner("Test Owner")
    dog = Pet("Test Dog", "Dog")
    me.add_pet(dog)
    
    # Add two tasks at the exact same time
    dog.add_task(Task("Morning Walk", "08:00", "Daily", "High"))
    dog.add_task(Task("Morning Meds", "08:00", "Daily", "High"))
    
    brain = Scheduler(me)
    all_tasks = brain.get_all_tasks()
    conflicts = brain.detect_conflicts(all_tasks)
    
    # Assert that exactly 1 conflict pairing was found
    assert len(conflicts) == 1
    # Assert the conflict involves our two overlapping tasks
    task1, task2 = conflicts[0]
    assert task1.time == "08:00" and task2.time == "08:00"

def test_recurrence_logic():
    """Verify a completed daily task successfully generates a clone for tomorrow."""
    me = Owner("Test Owner")
    brain = Scheduler(me)
    
    # Create a task for today
    today = datetime.now()
    task = Task("Daily Brushing", "10:00", "Daily", "Low")
    task.mark_complete()
    
    # Ask the brain to handle the recurrence
    next_task = brain.handle_recurrence(task, today)
    
    # Assert the new task is NOT the completed task, but a fresh copy
    assert next_task is not None
    assert next_task.completed is False