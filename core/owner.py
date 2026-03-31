import json
import os
from typing import List
from .pet import Pet
from .task import Task

class Owner:
    """The primary user who manages multiple pets."""
    def __init__(self, name: str, pets: List[Pet] = None):
        self.name = name
        self.pets = pets if pets is not None else []

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