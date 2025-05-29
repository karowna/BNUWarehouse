import unittest
from app.supplier import Supplier, SupplierManager
from app.item import Item  # Assuming the Item class is in item.py

class TestSupplierManager(unittest.TestCase):
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

    def test_update_profile(self):
        """Test the update_profile method."""
        supplier = Supplier("Steve", "steve@example.com", "1")

class TestItem(unittest.TestCase):
    def test_item_creation(self):
        """Test the creation of an Item."""
        supplier = Supplier("Steve", "steve@example.com", "1")
        item = Item(name="Dirt", description="Just dirt", price=10.0, supplier=supplier)
        
        self.assertIsInstance(item, Item)
        self.assertEqual(item.name, "Dirt")
        self.assertEqual(item.description, "Just dirt")
        self.assertEqual(item.price, 10.0)
        self.assertEqual(item.supplier, supplier)

if __name__ == "__main__":
    unittest.main()
