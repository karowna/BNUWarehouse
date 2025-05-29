import unittest
from app.supplier import Supplier, SupplierManager
from app.item import Item  # Assuming the Item class is in item.py
from unittest.mock import patch

class TestSupplier(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.supplier_manager = SupplierManager()

    def test_get_all_suppliers(self):
        """Test retrieving all suppliers."""
        self.assertEqual(self.supplier_manager.get_all_suppliers(), [])

        # Create a supplier and check if it appears in the list
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        suppliers = self.supplier_manager.get_all_suppliers()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0].name, "Steve")
        self.assertEqual(suppliers[0].email, "steve@example.com")
        self.assertTrue(suppliers[0].supplier_id.startswith("su_"))

    def test_create_supplier(self):
        """Test creating a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        self.assertIsInstance(supplier, Supplier)
        self.assertTrue(supplier.supplier_id.startswith("su_"))
        self.assertEqual(supplier.name, "Steve")
        self.assertEqual(supplier.email, "steve@example.com")

    def test_create_supplier_invalid_email(self):
        """Test creating a supplier with an invalid email format raises ValueError."""
        with self.assertRaises(ValueError):
            self.supplier_manager.create_supplier("Alice", "alice.com")

    def test_get_supplier_by_id(self):
        """Test fetching a supplier by ID."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        fetched_supplier = self.supplier_manager.get_supplier_by_id(supplier.supplier_id)
        
        self.assertEqual(fetched_supplier, supplier)
        self.assertEqual(fetched_supplier.supplier_id, supplier.supplier_id)

    def test_create_supplier_item(self):
        """Test creating an item for a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        item = self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Dirt", description="Just dirt", price=10.0)
        
        self.assertEqual(len(supplier.items_supplied), 1)
        self.assertEqual(supplier.items_supplied[0].name, "Dirt")
        self.assertEqual(supplier.items_supplied[0].description, "Just dirt")
        self.assertEqual(supplier.items_supplied[0].price, 10.0)

    def test_get_supplier_items(self):
        """Test retrieving items supplied by a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Dirt", description="Just dirt", price=10.0)
        self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Stone", description="Solid stone", price=20.0)
        items = self.supplier_manager.get_supplier_items(supplier.supplier_id)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Dirt")
        self.assertEqual(items[1].name, "Stone")

    def test_get_supplier_items_empty(self):
        """Test retrieving items from a supplier with no items."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        items = self.supplier_manager.get_supplier_items(supplier.supplier_id)
        self.assertEqual(len(items), 0)

    def test_get_supplier_items_invalid_id(self):
        """Test retrieving items for a non-existent supplier ID."""
        items = self.supplier_manager.get_supplier_items("su_999")  # ID not created
        self.assertEqual(items, [])

    def test_remove_item_from_supplier_success(self):
        """Test successfully removing an item from a supplier."""
        supplier = self.supplier_manager.create_supplier("Steve", "example@example.com")
        item = self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Dirt", description="Just dirt", price=10.0)

        self.assertIn(item, supplier.items_supplied)

        self.supplier_manager.remove_item_from_supplier(supplier.supplier_id, item)

        self.assertNotIn(item, supplier.items_supplied)

    def test_remove_nonexistent_item(self):
        """Test removing an item that does not exist in the supplier's inventory."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        item = Item(name="Dirt", description="Just dirt", price=10.0)  # Create an item not in the supplier's inventory
        with patch('builtins.print') as mock_print:
            supplier.remove_item(item)
            mock_print.assert_called_with(f"Item {item.name} not found in the list.")

    def test_remove_item_from_none_supplier(self):
        """Test removing an item from a supplier that does not exist."""
        self.supplier_manager.create_supplier("Steve", "example@example.com")
        item = Item(name="Dirt", description="Just dirt", price=10.0)

        with self.assertRaises(ValueError) as context:
            self.supplier_manager.remove_item_from_supplier("su_999", item)  # ID "su_999" does not exist

        self.assertIn("Supplier with ID su_999 not found", str(context.exception))

    def test_supplier_item_uniqueness(self):
        """Test that duplicate items are not allowed."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Dirt", description="Just dirt", price=10.0)

        with self.assertRaises(ValueError):
            self.supplier_manager.create_supplier_item(supplier.supplier_id, name="Dirt", description="Just dirt", price=10.0)
    
    def test_supplier_item_creation_on_none_existing_supplier(self):
        """Test creating an item for a non-existent supplier raises ValueError."""
        with self.assertRaises(ValueError):
            self.supplier_manager.create_supplier_item("su_999", name="Dirt", description="Just dirt", price=10.0)

    def test_supplier_item_create_with_none_item(self):
        """Test creating a supplier item with None as the item."""
        supplier = self.supplier_manager.create_supplier("Steve", "steve@example.com")
        with self.assertRaises(ValueError):
            self.supplier_manager.create_supplier_item(supplier.supplier_id, item=None)

    def test_get_role(self):
        """Test the get_role method."""
        supplier = Supplier("Steve", "steve@example.com")
        self.assertEqual(supplier.get_role(), "Supplier")

    def test_supplier_update_name(self):
        supplier = Supplier("Alice", "alice@example.com")
        supplier.update_profile(name="Alicia")
        self.assertEqual(supplier.name, "Alicia")
        self.assertEqual(supplier.email, "alice@example.com")

    def test_supplier_update_email(self):
        supplier = Supplier("Bob", "bob@example.com")
        supplier.update_profile(email="bobby@example.com")
        self.assertEqual(supplier.name, "Bob")
        self.assertEqual(supplier.email, "bobby@example.com")

        
if __name__ == "__main__":
    unittest.main()
