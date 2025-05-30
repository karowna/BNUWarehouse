import unittest
from app.item import Item


class MockSupplier:  # Mock class to simulate a supplier for testing purposes
    def __init__(self, name):
        self.name = name


class TestItem(unittest.TestCase):

    def test_str_representation(self):
        item = Item("Dirt", "Just dirt", 10.0)
        self.assertEqual(str(item), "Dirt - Just dirt (£10.00)")

    def test_repr_representation(self):
        item = Item("Stone", "Solid stone", 20.0)
        self.assertEqual(repr(item), "Item(Stone)")

    def test_hash_and_equality(self):
        item1 = Item("Dirt", "Just dirt", 10.0)
        item2 = Item("Dirt", "Just dirt", 10.0)
        item3 = Item("Sand", "Just sand", 5.0)

        self.assertEqual(item1, item2)
        self.assertNotEqual(item1, item3)
        self.assertEqual(hash(item1), hash(item2))
        self.assertNotEqual(hash(item1), hash(item3))

    def test_get_details_without_supplier(self):
        item = Item("Dirt", "Just dirt", 10.0)
        expected = "Dirt: Just dirt - £10.00"
        self.assertEqual(item.get_details(), expected)

    def test_get_details_with_supplier(self):
        supplier = MockSupplier("Steve")
        item = Item("Dirt", "Just dirt", 10.0, supplier=supplier)
        expected = "Dirt: Just dirt - £10.00 (Supplier: Steve)"
        self.assertEqual(item.get_details(), expected)

    def test_clone(self):
        original = Item("Dirt", "Just dirt", 10.0)
        clone = original.clone()

        # Check that the clone is equal in content
        self.assertEqual(clone.name, original.name)
        self.assertEqual(clone.description, original.description)
        self.assertEqual(clone.price, original.price)
        self.assertEqual(clone.supplier, original.supplier)

        # Check that the clone is a different object
        self.assertIsNot(clone, original)

        # Changing the clone's price should not affect the original
        clone.price = 20.0
        self.assertNotEqual(clone.price, original.price)


if __name__ == "__main__":
    unittest.main()
