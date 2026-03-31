from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from .owner import Owner
from .task import Task

class Scheduler:
    """The 'Brain' that organizes and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieves every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def handle_recurrence(self, task: Task, today: datetime) -> Optional[Task]:
        """Calculates the next instance of a task based on frequency."""
        if task.frequency not in ("Daily", "Weekly"):
            return None
            
        days_to_add = 1 if task.frequency == "Daily" else 7
        next_date = today + timedelta(days=days_to_add)
        
        return Task(
            description=task.description,
            time=task.time,
            frequency=task.frequency,
            priority=task.priority,
            target_date=next_date.strftime("%Y-%m-%d"),
            target_day=next_date.strftime("%A") if task.frequency == "Weekly" else task.target_day
        )

    def complete_task(self, task: Task, pet) -> None:
        """
        Marks a task as complete and automatically generates the next occurrence for recurring tasks.
        Uses Python's timedelta to calculate accurately.
        """
        task.mark_complete()
        
        # Calculate next occurrence if recurring
        if task.frequency in ("Daily", "Weekly"):
            days_to_add = 1 if task.frequency == "Daily" else 7
            
            # Determine base date
            if task.target_date:
                base_date = datetime.strptime(task.target_date, "%Y-%m-%d")
            else:
                base_date = datetime.now()
                
            next_date = base_date + timedelta(days=days_to_add)
            
            # Clone and append the future task
            new_task = Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                priority=task.priority,
                target_date=next_date.strftime("%Y-%m-%d"),
                target_day=next_date.strftime("%A") if task.frequency == "Weekly" else task.target_day
            )
            pet.add_task(new_task)

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
        """Sorts tasks strictly chronologically by time (Used for Single Day view)."""
        return sorted(tasks, key=lambda x: x.time)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts by Priority (High -> Medium -> Low), then by time (Used for Single Day view)."""
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        return sorted(tasks, key=lambda x: (priority_map.get(x.priority.capitalize(), 3), x.time))

    # --- NEW: MASTER LIST SORTING LOGIC ---

    def sort_master_list_by_date(self, tasks: List[Task]) -> List[Task]:
        """Sorts all tasks: Daily first, then Weekly (by day), then Once (by exact date)."""
        def sort_key(task):
            # 1. Frequency order: Daily (0), Weekly (1), Once (2)
            freq_order = {"Daily": 0, "Weekly": 1, "Once": 2}
            f_val = freq_order.get(task.frequency, 3)
            
            # 2. Date order: If it has a date, use it. Otherwise, push to end.
            d_val = task.target_date if task.target_date else "9999-12-31" 
            
            # 3. Day of week order for weekly tasks
            day_order = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7, None: 8}
            w_val = day_order.get(task.target_day, 8)
            
            # Sort by Frequency -> Date -> Day of Week -> Time
            return (f_val, d_val, w_val, task.time)

        return sorted(tasks, key=sort_key)

    def sort_master_list_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sorts all tasks strictly by Priority first, then applies the date logic."""
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        
        def sort_key(task):
            # 1. Priority is the absolute most important sorting factor here
            p_val = priority_map.get(task.priority.capitalize(), 3)
            
            # 2. Then group by frequency
            freq_order = {"Daily": 0, "Weekly": 1, "Once": 2}
            f_val = freq_order.get(task.frequency, 3)
            
            # 3. Then by date
            d_val = task.target_date if task.target_date else "9999-12-31"
            
            return (p_val, f_val, d_val, task.time)
            
        return sorted(tasks, key=sort_key)

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Finds tasks scheduled for the exact same time."""
        conflicts = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks) - 1):
            if sorted_tasks[i].time == sorted_tasks[i+1].time:
                conflicts.append((sorted_tasks[i], sorted_tasks[i+1]))
        return conflicts