import unittest
from customer import Customer, CustomerManager

class TestCustomerManager(unittest.TestCase):
    """Unit tests for the CustomerManager and Customer classes."""

    def setUp(self):
        self.manager = CustomerManager()
        self.customer = self.manager.create_customer("Bob", "bob@example.com", "CUST001")

    def test_create_customer(self):
        self.assertEqual(self.customer.name, "Bob")
        self.assertEqual(self.customer.email, "bob@example.com")
        self.assertEqual(self.customer.customer_id, "CUST001")
        self.assertIn("CUST001", self.manager.customers)

    def test_create_duplicate_customer_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.create_customer("Bob", "bob@example.com", "CUST001")

    def test_get_customer_by_id(self):
        customer = self.manager.get_customer_by_id("CUST001")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Bob")

    def test_update_customer(self):
        self.manager.update_customer("CUST001", name="Bob Smith", email="bob.smith@example.com")
        customer = self.manager.get_customer_by_id("CUST001")
        self.assertEqual(customer.name, "Bob Smith")
        self.assertEqual(customer.email, "bob.smith@example.com")

    def test_update_nonexistent_customer_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.update_customer("CUST999", name="Ghost")

    def test_delete_customer(self):
        self.manager.delete_customer("CUST001")
        self.assertIsNone(self.manager.get_customer_by_id("CUST001"))

    def test_delete_nonexistent_customer_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.delete_customer("CUST999")

    def test_customer_get_role(self):
        self.assertEqual(self.customer.get_role(), "Customer")

if __name__ == '__main__':
    unittest.main()
