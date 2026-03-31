# tests/test_pawpal.py
from pawpal_system import Pet, Task

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task("Morning Walk", "08:00", "Daily", "High")
    
    # It should be False initially
    assert task.completed is False  
    
    # Mark it complete
    task.mark_complete()
    
    # It should now be True
    assert task.completed is True      

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    dog = Pet(name="Buddy", species="Dog")
    task = Task("Evening Feed", "18:00", "Daily", "Medium")
    
    initial_count = len(dog.tasks) # Should be 0
    dog.add_task(task)
    new_count = len(dog.tasks)     # Should be 1
    
    # The new count should be 1 higher than the initial count
    assert new_count == initial_count + 1
    # The task inside the pet's list should be the exact task we added
    assert dog.tasks[0] == task