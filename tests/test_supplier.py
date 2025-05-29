import unittest
from app.supplier import Supplier, SupplierManager
from app.item import Item  # Assuming the Item class is in item.py
from unittest.mock import patch

class TestSupplier(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.supplier_manager = SupplierManager()

    def test_create_supplier(self):
        """Test creating a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com", "1")
        self.assertIsInstance(supplier, Supplier)
        self.assertEqual(supplier.supplier_id, "1")
        self.assertEqual(supplier.name, "Steve")
        self.assertEqual(supplier.email, "steve@example.com")

    def test_create_supplier_item(self):
        """Test creating an item for a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com", "1")
        item = self.supplier_manager.create_supplier_item("1", name="Dirt", description="Just dirt", price=10.0)
        
        self.assertEqual(len(supplier.items_supplied), 1)
        self.assertEqual(supplier.items_supplied[0].name, "Dirt")
        self.assertEqual(supplier.items_supplied[0].description, "Just dirt")
        self.assertEqual(supplier.items_supplied[0].price, 10.0)

    def test_get_supplier_by_id(self):
        """Test fetching a supplier by ID."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com", "1")
        fetched_supplier = self.supplier_manager.get_supplier_by_id("1")
        
        self.assertEqual(fetched_supplier, supplier)
        self.assertEqual(fetched_supplier.supplier_id, "1")

    def test_remove_item(self):
        """Test removing an item from a supplier's inventory."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com", "1")
        item = self.supplier_manager.create_supplier_item("1", name="Dirt", description="Just dirt", price=10.0)
    
        self.assertEqual(len(supplier.items_supplied), 1)
        
        supplier.remove_item(item)
        
        self.assertEqual(len(supplier.items_supplied), 0)

    def test_supplier_item_uniqueness(self):
        """Test that duplicate items are not allowed."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com", "1")
        self.supplier_manager.create_supplier_item("1", name="Dirt", description="Just dirt", price=10.0)

        # Try creating a duplicate item with the same name and description
        with self.assertRaises(ValueError):
            self.supplier_manager.create_supplier_item("1", name="Dirt", description="Just dirt", price=10.0)

    def test_get_role(self):
        """Test the get_role method."""
        supplier = Supplier("Steve", "steve@example.com", "1")
        self.assertEqual(supplier.get_role(), "Supplier")

    def test_supplier_update_name(self):
        supplier = Supplier("Alice", "alice@example.com", "1")
        supplier.update_profile(name="Alicia")
        self.assertEqual(supplier.name, "Alicia")
        self.assertEqual(supplier.email, "alice@example.com")

    def test_supplier_update_email(self):
        supplier = Supplier("Bob", "bob@example.com", "1")
        supplier.update_profile(email="bobby@example.com")
        self.assertEqual(supplier.name, "Bob")
        self.assertEqual(supplier.email, "bobby@example.com")
if __name__ == "__main__":
    unittest.main()
