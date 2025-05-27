from abc import ABC # Abstract Base Class for Person, we will never create a Person directly

class Person(ABC):
    def __init__(self, person_id, name, phone, email):
        """ Initializes a Person object with name, phone, email, and id."""
        self.name = name
        self.phone = phone
        self.email = email
        self.person_id = person_id

    