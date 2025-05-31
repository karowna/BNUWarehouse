# tests/test_person.py

import unittest
from app.person import Person


class TestPersonInstantiation(unittest.TestCase):
    """Unit tests for the Person class. We need to make sure we cannot instantiate a Person directly since it is an abstract class."""

    def test_person_instantiation_raises_type_error(self):
        with self.assertRaises(TypeError):
            Person("P001", "John Doe", "john@example.com")


if __name__ == "__main__":
    unittest.main()
