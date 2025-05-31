# tests/test_order.py

import unittest
from app.order import Order
from app.item import Item
from app.customer import Customer


class TestOrderRepr(
    unittest.TestCase
):  # Only have this left to test, the rest of the code is already covered in other files.
    def test_order_repr(self):
        """Test the string representation of an Order."""
        item = Item("Dirt", "Just dirt", 10.0)
        customer = Customer("bkar", "bkarowna@gmail.com")
        order = Order(item=item, quantity=5, buyer=customer, seller="Warehouse")
        expected_repr = f"Order #{order.order_id} ({item.name}, Qty: {order.quantity}, Buyer: {customer.name}, Status: {order.status})"
        self.assertEqual(repr(order), expected_repr)
