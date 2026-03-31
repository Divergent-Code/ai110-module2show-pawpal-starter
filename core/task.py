"""
core/task.py

Defines the foundational Data Model for the PawPal+ system using Python's `dataclass`.
Provides automatic `__init__`, `__repr__`, and equality methods with minimal boilerplate.
"""
from dataclasses import dataclass, asdict
from typing import Dict, Optional


@dataclass
class Task:
    """Represents a specific care activity for a pet."""
    description: str
    time: str                       # Format: "HH:MM"
    frequency: str                  # "Daily", "Weekly", "Once"
    priority: str                   # "High", "Medium", "Low"
    
    target_date: Optional[str] = None  # Format: "YYYY-MM-DD" (Used for "Once")
    target_day: Optional[str] = None   # Format: "Monday" (Used for "Weekly")
    completed: bool = False

    def mark_complete(self) -> None:
        """Sets the task status to completed."""
        self.completed = True

    def to_dict(self) -> Dict:
        """Serializes the Task to a dictionary for JSON compatibility."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        """Creates a Task instance from a dictionary."""
        return cls(**data)
