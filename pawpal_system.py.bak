import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict

@dataclass
class Task:
    """Represents a specific care activity for a pet."""
    description: str
    time: str  # Format: "HH:MM"
    frequency: str
    priority: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Sets the task status to completed."""
        self.completed = True

    def next_occurrence(self, today: datetime) -> datetime:
        """Calculates the next datetime this task should occur."""
        try:
            hour, minute = map(int, self.time.split(':'))
            occurrence = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if occurrence < datetime.now():
                # If the time has passed today, schedule for tomorrow
                occurrence += timedelta(days=1)
            return occurrence
        except ValueError:
            return today

    def to_dict(self) -> Dict:
        """Converts task data to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Creates a Task instance from a dictionary."""
        return cls(**data)

@dataclass
class Pet:
    """Represents an individual pet and its associated tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to this pet."""
        self.tasks.append(task)

    def to_dict(self) -> Dict:
        """Converts pet data and nested tasks to a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Pet':
        """Creates a Pet instance (and its Tasks) from a dictionary."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(name=data["name"], species=data["species"], tasks=tasks)

class Owner:
    """The primary user who manages multiple pets."""
    def __init__(self, name: str, pets: List[Pet] = None):
        self.name = name
        self.pets = pets if pets else []

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to the owner's profile."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Aggregates all tasks from all pets owned."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def save_to_json(self, filename: str) -> None:
        """Saves owner, pets, and tasks to a JSON file."""
        data = {
            "name": self.name,
            "pets": [p.to_dict() for p in self.pets]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_json(cls, filename: str) -> 'Owner':
        """Loads data from a JSON file and reconstructs objects."""
        if not os.path.exists(filename):
            return cls(name="Default Owner")
            
        with open(filename, 'r') as f:
            data = json.load(f)
        
        owner = cls(name=data.get("name", "Unknown"))
        owner.pets = [Pet.from_dict(p) for p in data.get("pets", [])]
        return owner

class Scheduler:
    """The 'Brain' that organizes and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks strictly chronologically by time."""
        return sorted(tasks, key=lambda x: x.time)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts by Priority (High -> Medium -> Low), then by time."""
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        # Safely default to 3 if priority is unrecognized
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