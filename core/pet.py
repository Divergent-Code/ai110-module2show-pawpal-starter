"""
core/pet.py

Defines the entity-level `Pet` class which acts as a container for tasks.
Architecturally, this forms a 1-to-many composition relationship between 
a single Pet and its `List[Task]`.
"""
from dataclasses import dataclass, field
from typing import List, Dict
from .task import Task

@dataclass
class Pet:
    """Represents an individual pet and its associated tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to this pet by appending it to the internal list."""
        self.tasks.append(task)

    def to_dict(self) -> Dict:
        """Converts pet data and nested tasks to a dictionary for saving."""
        return {
            "name": self.name,
            "species": self.species,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Pet':
        """Creates a Pet instance (and its Tasks) from a dictionary."""
        tasks_list = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(name=data["name"], species=data["species"], tasks=tasks_list)