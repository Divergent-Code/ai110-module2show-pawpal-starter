from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from datetime import datetime
import json

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

    def to_dict(self) -> Dict:
        """Converts task data to a dictionary (returns a safe copy)."""
        return dict(self.__dict__)

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """Creates a Task instance from a dictionary."""
        return Task(**data)

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

    @staticmethod
    def from_dict(data: Dict) -> 'Pet':
        """Creates a Pet instance (and its Tasks) from a dictionary."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return Pet(name=data["name"], species=data["species"], tasks=tasks)

@dataclass
class Owner:
    """The primary user who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to the owner's profile."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Aggregates all tasks from all pets owned."""
        return [task for pet in self.pets for task in pet.tasks]

    def to_dict(self) -> Dict:
        """Converts owner data and all nested pets/tasks to a dictionary."""
        return {
            "name": self.name,
            "pets": [p.to_dict() for p in self.pets]
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Owner':
        """Creates an Owner instance (and all nested Pets/Tasks) from a dictionary."""
        pets = [Pet.from_dict(p) for p in data.get("pets", [])]
        return Owner(name=data["name"], pets=pets)

class Scheduler:
    """The 'Brain' that organizes and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_sorted_schedule(self) -> List[Task]:
        """Returns all tasks sorted by time."""
        tasks = self.owner.get_all_tasks()
        # Simple string-based time sorting (assumes 24h format "HH:MM")
        return sorted(tasks, key=lambda x: x.time)