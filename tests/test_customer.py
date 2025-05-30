import unittest
from app.customer import Customer, CustomerManager
from app.order import Order
from app.item import Item

class TestCustomerManager(unittest.TestCase):
    """Unit tests for the CustomerManager and Customer classes."""

    def setUp(self):
        """Set up for the tests. Create a CustomerManager and a sample customer."""
        self.manager = CustomerManager()
        self.customer = self.manager.create_customer("Bob", "bob@example.com")

    def test_add_order_appends_to_history(self):
        """Test that add_order correctly appends an order to the customer's history."""
        customer = Customer("Alice", "alice@example.com")
        item = Item("Dirt", "Just dirt", 10.0)
        order = Order(item=item, quantity=2, buyer=customer, seller="Warehouse")

        customer.add_order(order)

        self.assertIn(order, customer.order_history)
        self.assertEqual(len(customer.order_history), 1)

    def test_view_order_history_returns_correct_list(self):
        """Test that view_order_history returns the correct list of orders."""
        customer = Customer("Alice", "alice@example.com")
        item = Item("Stone", "Solid stone", 15.0)
        order = Order(item=item, quantity=1, buyer=customer, seller="Warehouse")

        customer.add_order(order)
        history = customer.view_order_history()

        self.assertEqual(history, [order])

    def test_create_customer(self):
        """Test that a customer is created properly."""
        self.assertEqual(self.customer.name, "Bob")
        self.assertEqual(self.customer.email, "bob@example.com")
        self.assertTrue(self.customer.customer_id.startswith("cu_"))
        self.assertIn(self.customer.customer_id, self.manager.customers)

    def test_create_customer_wrong_email_format(self):
        """Test that creating a customer with an invalid email format raises ValueError."""
        with self.assertRaises(ValueError):
            self.manager.create_customer("Alice", "alice.com")

    def test_get_customer_by_id(self):
        """Test retrieving a customer by their ID."""
        customer = self.manager.get_customer_by_id(self.customer.customer_id)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Bob")

    def test_update_customer_profile(self):
        """Test updating a customer's profile (name and email)."""
        self.customer.update_profile(name="Bob Smith", email="bob.smith@example.com")
        customer = self.manager.get_customer_by_id(self.customer.customer_id)
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
        self.manager.delete_customer(self.customer.customer_id)
        self.assertIsNone(self.manager.get_customer_by_id(self.customer.customer_id))

    def test_delete_nonexistent_customer_raises_error(self):
        """Test that deleting a non-existent customer raises a ValueError."""
        with self.assertRaises(ValueError):
            self.manager.delete_customer("CUST999")

    def test_customer_get_role(self):
        """Test the get_role method to ensure the customer role is returned correctly."""
        self.assertEqual(self.customer.get_role(), "Customer")

    def test_get_customer_by_id_not_found(self):
        """Test that get_customer_by_id returns None when the customer ID is not found."""
        non_existent_id = "cu_9999"
        customer = self.manager.get_customer_by_id(non_existent_id)
        self.assertIsNone(customer)

    def test_view_order_history_empty(self):
        """Test that view_order_history returns None when there is no order history."""
        customer = Customer("Charlie", "charlie@example.com")
        history = customer.view_order_history()
        self.assertIsNone(history)


if __name__ == '__main__':
    unittest.main()
