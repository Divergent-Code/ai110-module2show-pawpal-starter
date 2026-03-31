from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from datetime import datetime

@dataclass
class Task:
    """Represents a specific care activity for a pet."""
    description: str
    time: str
    frequency: str
    priority: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Sets the task status to completed."""
        pass

    def next_occurrence(self, today: datetime) -> datetime:
        """Calculates the next date/time this task should occur."""
        pass

    def to_dict(self) -> Dict:
        """Converts task data to a dictionary for JSON storage."""
        pass

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """Creates a Task instance from a dictionary."""
        pass

@dataclass
class Pet:
    """Represents an individual pet and its associated tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to this pet."""
        pass

    def to_dict(self) -> Dict:
        """Converts pet data to a dictionary."""
        pass

    @staticmethod
    def from_dict(data: Dict) -> 'Pet':
        """Creates a Pet instance from a dictionary."""
        pass

@dataclass
class Owner:
    """The primary user who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to the owner's profile."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Aggregates all tasks from all pets owned."""
        pass

    def save_to_json(self, filename: str) -> None:
        """Serializes the entire owner object tree to a JSON file."""
        pass

    @classmethod
    def load_from_json(cls, filename: str) -> 'Owner':
        """Loads owner and pet data from a JSON file."""
        pass

class Scheduler:
    """Logic-heavy class for managing time and task conflicts."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieves tasks via the Owner object."""
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Returns tasks ordered by their scheduled time."""
        pass

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Returns tasks ordered by priority, then chronologically."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple]:
        """Identifies overlapping tasks in the schedule."""
        pass

    def next_available_slot(self, tasks: List[Task], duration_minutes: int) -> Optional[str]:
        """Finds a free gap in the schedule for a new task."""
        pass

    def handle_recurrence(self, task: Task, today: datetime) -> Optional[Task]:
        """Generates the next task instance if it is recurring."""
        pass