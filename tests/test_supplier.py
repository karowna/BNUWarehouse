import unittest
from person import Person
from supplier import Supplier, SupplierManager

class TestSupplierManager(unittest.TestCase):

    def setUp(self):
        self.manager = SupplierManager()
        self.supplier = self.manager.create_supplier("Alice", "alice@example.com", "SUP001")

    def test_create_supplier(self):
        self.assertEqual(self.supplier.name, "Alice")
        self.assertEqual(self.supplier.email, "alice@example.com")
        self.assertEqual(self.supplier.supplier_id, "SUP001")
        self.assertIn("SUP001", self.manager.suppliers)

    def test_create_duplicate_supplier_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.create_supplier("Alice", "alice@example.com", "SUP001")

    def test_get_supplier_by_id(self):
        supplier = self.manager.get_supplier_by_id("SUP001")
        self.assertIsNotNone(supplier)
        self.assertEqual(supplier.name, "Alice")

    def test_update_supplier(self):
        self.manager.update_supplier("SUP001", name="Alice Smith", email="alice.smith@example.com")
        supplier = self.manager.get_supplier_by_id("SUP001")
        self.assertEqual(supplier.name, "Alice Smith")
        self.assertEqual(supplier.email, "alice.smith@example.com")

    def test_update_nonexistent_supplier_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.update_supplier("SUP999", name="Ghost")

    def test_delete_supplier(self):
        self.manager.delete_supplier("SUP001")
        self.assertIsNone(self.manager.get_supplier_by_id("SUP001"))

    def test_delete_nonexistent_supplier_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.delete_supplier("SUP999")

if __name__ == '__main__':
    unittest.main()
