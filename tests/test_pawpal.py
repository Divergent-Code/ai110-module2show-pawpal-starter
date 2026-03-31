# tests/test_pawpal.py
from datetime import datetime, timedelta
from core import Owner, Pet, Task, Scheduler

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task("Morning Walk", "08:00", "Daily", "High")
    assert task.completed is False  
    task.mark_complete()
    assert task.completed is True      

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    dog = Pet(name="Buddy", species="Dog")
    task = Task("Evening Feed", "18:00", "Daily", "Medium")
    initial_count = len(dog.tasks)
    dog.add_task(task)
    new_count = len(dog.tasks)
    assert new_count == initial_count + 1
    assert dog.tasks[0] == task

def test_sorting_correctness():
    """Verify that tasks are returned in exact chronological order."""
    owner = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    owner.add_pet(dog)
    
    # Add tasks out of chronological order
    dog.add_task(Task("Bedtime", "22:00", "Daily", "Low"))
    dog.add_task(Task("Breakfast", "07:00", "Daily", "High"))
    dog.add_task(Task("Lunch", "12:00", "Daily", "Medium"))
    
    brain = Scheduler(owner)
    unsorted = brain.get_all_tasks()
    sorted_tasks = brain.sort_by_time(unsorted)
    
    # Check that they sorted themselves into 07:00 -> 12:00 -> 22:00
    assert sorted_tasks[0].description == "Breakfast"
    assert sorted_tasks[1].description == "Lunch"
    assert sorted_tasks[2].description == "Bedtime"
    
def test_recurrence_logic():
    """Confirm that marking a daily task complete generates tomorrow's instance."""
    owner = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    owner.add_pet(dog)
    
    brain = Scheduler(owner)
    
    base_task = Task("Morning Walk", "08:00", "Daily", "High", target_date="2026-06-01")
    dog.add_task(base_task)
    
    initial_count = len(dog.tasks) # 1
    
    # Trigger completion
    brain.complete_task(base_task, dog)
    
    new_count = len(dog.tasks) # Expect 2
    assert new_count == initial_count + 1
    assert base_task.completed is True
    
    # The new task should be identical but exactly 1 day shifted forward
    new_task = dog.tasks[1]
    assert new_task.description == "Morning Walk"
    assert new_task.completed is False
    assert new_task.target_date == "2026-06-02"
    
def test_conflict_detection():
    """Verify that the Scheduler strictly flags duplicate overlapping times."""
    owner = Owner(name="Alex")
    dog = Pet(name="Buddy", species="Dog")
    owner.add_pet(dog)
    
    brain = Scheduler(owner)
    
    # Intentional exact overlap at 08:00
    t1 = Task("Morning Walk", "08:00", "Daily", "High")
    t2 = Task("Morning Meds", "08:00", "Once", "High")
    t3 = Task("Lunch", "12:00", "Daily", "Medium")
    
    dog.add_task(t1)
    dog.add_task(t2)
    dog.add_task(t3)
    
    conflicts = brain.detect_conflicts(brain.get_all_tasks())
    
    # It should return a list of exactly 1 conflict tuple containing t1 and t2
    assert len(conflicts) == 1
    assert conflicts[0][0].time == "08:00"
    assert conflicts[0][1].time == "08:00"