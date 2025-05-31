# /app/person.py

from abc import (
    ABC,
    abstractmethod,
)  # Abstract Base Class for Person, we will never create a Person directly


class Person(ABC):
    def __init__(self, name, email):
        """Initializes a Person object with name and email."""
        if "@" not in email:
            raise ValueError(
                "Invalid email address: must contain '@'"
            )  # Validation at the higher level inside the constructor

        self.name = name  # Attributes
        self.email = email

    @abstractmethod
    def get_role(self):  # Untestable abstract method, must be implemented by subclasses
        """Return the role of the person (e.g., Customer, Supplier)."""
        pass

    @abstractmethod
    def generate_id(
        self,
    ):  # Abstract method to be implemented by subclasses for ID generation
        """Generate a unique ID for the person."""
        pass

    def update_profile(self, name=None, email=None):
        """Allow the person to update their profile."""
        if name:
            self.name = name
        if email:
            self.email = email
