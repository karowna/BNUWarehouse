import unittest
from app.customer import Customer, CustomerManager

class TestCustomerManager(unittest.TestCase):
    """Unit tests for the CustomerManager and Customer classes."""

    def setUp(self):
        """Set up for the tests. Create a CustomerManager and a sample customer."""
        self.manager = CustomerManager()
        self.customer = self.manager.create_customer("Bob", "bob@example.com", "CUST001")

    def test_create_customer(self):
        """Test that a customer is created properly."""
        self.assertEqual(self.customer.name, "Bob")
        self.assertEqual(self.customer.email, "bob@example.com")
        self.assertEqual(self.customer.customer_id, "CUST001")
        self.assertIn("CUST001", self.manager.customers)

    def test_create_duplicate_customer_raises_error(self):
        """Test that creating a customer with an existing ID raises a ValueError."""
        with self.assertRaises(ValueError):
            self.manager.create_customer("Bob", "bob@example.com", "CUST001")

    def test_get_customer_by_id(self):
        """Test retrieving a customer by their ID."""
        customer = self.manager.get_customer_by_id("CUST001")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Bob")

    def test_update_customer_profile(self):
        """Test updating a customer's profile (name and email)."""
        self.customer.update_profile(name="Bob Smith", email="bob.smith@example.com")
        customer = self.manager.get_customer_by_id("CUST001")
        self.assertEqual(customer.name, "Bob Smith")
        self.assertEqual(customer.email, "bob.smith@example.com")

    def test_update_customer_profile_no_changes(self):
        """Test updating a customer's profile with no changes."""
        initial_name = self.customer.name
        initial_email = self.customer.email
        self.customer.update_profile()  # No updates
        self.assertEqual(self.customer.name, initial_name)
        self.assertEqual(self.customer.email, initial_email)

    def test_update_customer_profile_partial_update(self):
        """Test updating only one field of the profile (email)."""
        self.customer.update_profile(email="bob.newemail@example.com")
        self.assertEqual(self.customer.name, "Bob")  # Name should remain the same
        self.assertEqual(self.customer.email, "bob.newemail@example.com")

    def test_delete_customer(self):
        """Test that deleting a customer works as expected."""
        self.manager.delete_customer("CUST001")
        self.assertIsNone(self.manager.get_customer_by_id("CUST001"))

    def test_delete_nonexistent_customer_raises_error(self):
        """Test that deleting a non-existent customer raises a ValueError."""
        with self.assertRaises(ValueError):
            self.manager.delete_customer("CUST999")

    def test_customer_get_role(self):
        """Test the get_role method to ensure the customer role is returned correctly."""
        self.assertEqual(self.customer.get_role(), "Customer")

if __name__ == '__main__':
    unittest.main()
