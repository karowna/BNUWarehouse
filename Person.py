from abc import ABC, abstractmethod # Abstract Base Class for Person, we will never create a Person directly

class Person(ABC):
    def __init__(self, person_id, name, email): # Constructor
        """ Initializes a Person object with name, phone, email, and id."""
        self.name = name # Attributes
        self.email = email
        self.person_id = person_id

    @abstractmethod
    def get_role(self):
        """Return the role of the person (e.g., Customer, Supplier)."""
        pass
