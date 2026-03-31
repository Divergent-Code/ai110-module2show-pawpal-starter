"""
core/scheduler.py

Serves as the algorithmic engine of PawPal+. Encapsulates all scheduling, sorting, 
and conflict detection logic. Designed for performance with O(N log N) efficiency 
using Python's native TimSort.
"""
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from .owner import Owner
from .task import Task


# Priority mapping constants
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
FREQ_ORDER = {"Daily": 0, "Weekly": 1, "Once": 2}
DAY_ORDER = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, 
             "Friday": 5, "Saturday": 6, "Sunday": 7}


class Scheduler:
    """The 'Brain' that organizes and manages tasks across pets."""
    
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieves every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def _calculate_next_occurrence(self, task: Task, base_date: datetime) -> Task:
        """Helper to calculate the next occurrence of a recurring task."""
        days_to_add = 1 if task.frequency == "Daily" else 7
        next_date = base_date + timedelta(days=days_to_add)
        
        return Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            priority=task.priority,
            target_date=next_date.strftime("%Y-%m-%d"),
            target_day=next_date.strftime("%A") if task.frequency == "Weekly" else task.target_day
        )

    def handle_recurrence(self, task: Task, today: datetime) -> Optional[Task]:
        """Calculates the next instance of a task based on frequency."""
        if task.frequency not in ("Daily", "Weekly"):
            return None
            
        return self._calculate_next_occurrence(task, today)

    def complete_task(self, task: Task, pet) -> None:
        """
        Marks a task as complete and generates the next occurrence for recurring tasks.
        """
        task.mark_complete()
        
        if task.frequency not in ("Daily", "Weekly"):
            return
            
        base_date = (datetime.strptime(task.target_date, "%Y-%m-%d") 
                     if task.target_date else datetime.now())
        
        pet.add_task(self._calculate_next_occurrence(task, base_date))

    def get_schedule_for_date(self, target_date: datetime) -> List[Task]:
        """Filters tasks to show only what is relevant for a specific date."""
        date_str = target_date.strftime("%Y-%m-%d")
        day_str = target_date.strftime("%A")

        return [
            task for task in self.get_all_tasks()
            if (task.frequency == "Daily" or
                (task.frequency == "Weekly" and task.target_day == day_str) or
                (task.frequency == "Once" and task.target_date == date_str))
        ]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks chronologically by time."""
        return sorted(tasks, key=lambda x: x.time)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts by Priority (High -> Medium -> Low), then by time."""
        return sorted(tasks, key=lambda x: (PRIORITY_ORDER.get(x.priority, 3), x.time))

    def sort_master_list_by_date(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks: Daily first, then Weekly (by day), then Once (by date)."""
        def sort_key(task: Task) -> Tuple:
            return (
                FREQ_ORDER.get(task.frequency, 3),
                task.target_date or "9999-12-31",
                DAY_ORDER.get(task.target_day, 8),
                task.time
            )
        return sorted(tasks, key=sort_key)

    def sort_master_list_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sorts by Priority first, then by frequency and date."""
        def sort_key(task: Task) -> Tuple:
            return (
                PRIORITY_ORDER.get(task.priority, 3),
                FREQ_ORDER.get(task.frequency, 3),
                task.target_date or "9999-12-31",
                task.time
            )
        return sorted(tasks, key=sort_key)

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Finds tasks scheduled for the exact same time."""
        sorted_tasks = self.sort_by_time(tasks)
        return [
            (sorted_tasks[i], sorted_tasks[i + 1])
            for i in range(len(sorted_tasks) - 1)
            if sorted_tasks[i].time == sorted_tasks[i + 1].time
        ]
