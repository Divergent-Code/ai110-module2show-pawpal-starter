from typing import List, Tuple, Optional
from datetime import datetime
from .owner import Owner
from .task import Task

class Scheduler:
    """The 'Brain' that organizes and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieves every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def get_schedule_for_date(self, target_date_obj: datetime) -> List[Task]:
        """Filters tasks to only show what is relevant for a specific date."""
        all_tasks = self.get_all_tasks()
        filtered_tasks = []
        
        target_date_str = target_date_obj.strftime("%Y-%m-%d")
        target_day_str = target_date_obj.strftime("%A") 

        for task in all_tasks:
            if task.frequency == "Daily":
                filtered_tasks.append(task)
            elif task.frequency == "Weekly" and task.target_day == target_day_str:
                filtered_tasks.append(task)
            elif task.frequency == "Once" and task.target_date == target_date_str:
                filtered_tasks.append(task)
                
        return filtered_tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks strictly chronologically by time."""
        return sorted(tasks, key=lambda x: x.time)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts by Priority (High -> Medium -> Low), then by time."""
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        return sorted(tasks, key=lambda x: (priority_map.get(x.priority.capitalize(), 3), x.time))

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Finds tasks scheduled for the exact same time."""
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks) - 1):
            if sorted_tasks[i].time == sorted_tasks[i+1].time:
                conflicts.append((sorted_tasks[i], sorted_tasks[i+1]))
        return conflicts

    def next_available_slot(self, tasks: List[Task], duration_minutes: int) -> Optional[str]:
        """Placeholder: Finds the next gap in the schedule."""
        # For a full implementation, this would parse times and find a gap > duration_minutes.
        # Returning a default safe slot for demonstration.
        return "12:00"

    def handle_recurrence(self, task: Task, today: datetime) -> Optional[Task]:
        """Calculates the next instance of a task based on frequency."""
        # This aligns with the UML; actual logic depends on how you want to clone the task.
        return task