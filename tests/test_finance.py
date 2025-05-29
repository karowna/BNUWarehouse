import unittest
import io
from unittest.mock import patch
from app.order import Order
from app.item import Item
from app.supplier import Supplier, SupplierManager
from app.warehouse import Warehouse
from app.customer import Customer, CustomerManager
from app.finance import FinanceCompiler

class TestFinanceCompiler(unittest.TestCase):

    def setUp(self):
        # Setup warehouse instance
        self.warehouse = Warehouse(name="Main Warehouse")
        
        # Create the managers
        self.customer_manager = CustomerManager()
        self.supplier_manager = SupplierManager()

        # Create customer and supplier using the managers
        self.customer = self.customer_manager.create_customer(name="Alice", email="alice@example.com")
        self.supplier = self.supplier_manager.create_supplier(name="Supplier A", email="supplier@example.com")

        # Create some items
        self.item1 = Item(name="Widget", description="A small widget", price=19.99, supplier=self.supplier)
        self.item2 = Item(name="Gadget", description="A useful gadget", price=24.99, supplier=self.supplier)

        # Create orders using the created customer and supplier
        self.order1 = Order(item=self.item1, quantity=5, buyer=self.customer, seller=self.warehouse)  # Customer ordering from warehouse
        self.order2 = Order(item=self.item2, quantity=2, buyer=self.warehouse, seller=self.supplier)  # Warehouse ordering from supplier
        self.orders = [self.order1, self.order2]

        # Initialize FinanceCompiler
        self.finance_compiler = FinanceCompiler(self.orders)

    def test_total_customer_revenue(self):
        """Test that total customer revenue is calculated correctly."""
        self.assertEqual(self.finance_compiler.total_customer_revenue(), self.order1.total_price)

    def test_total_supplier_costs(self):
        """Test that total supplier costs are calculated correctly."""
        self.assertEqual(self.finance_compiler.total_supplier_costs(), self.order2.total_price)

    def test_calculate_profit(self):
        """Test that the profit is correctly calculated."""
        expected_profit = self.order1.total_price - self.order2.total_price
        self.assertEqual(self.finance_compiler.calculate_profit(), expected_profit)

    def test_export_orders_to_csv(self):
        """Test that orders are exported correctly to a CSV."""
        file_path = "test_orders.csv"
        self.finance_compiler.export_orders_to_csv(self.orders, file_path)
        # Check that the file exists and contains data (basic check)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.assertGreater(len(lines), 1)  # Should have more than just the header
        # Optionally, check specific contents of the file

    def test_summarise_orders(self):
        """Test that orders are correctly summarized."""
        summary = self.finance_compiler.summarise_orders()
        self.assertEqual(len(summary), 2)  # We have 2 orders
        self.assertIn("order_id", summary[0])
        self.assertIn("total_price", summary[0])
        self.assertIn("item_name", summary[0])


    def test_get_customer_orders(self):
        """Test that customer orders are correctly returned."""
        customer_orders = self.finance_compiler.get_customer_orders()
        self.assertEqual(len(customer_orders), 1)  # Only one customer order
        self.assertEqual(customer_orders[0], self.order1)

    def test_get_supplier_orders(self):
        """Test that supplier orders are correctly returned."""
        supplier_orders = self.finance_compiler.get_supplier_orders()
        self.assertEqual(len(supplier_orders), 1)  # Only one supplier order
        self.assertEqual(supplier_orders[0], self.order2)

    def test_get_all_orders(self):
        """Test that all orders are correctly returned."""
        all_orders = self.finance_compiler.get_all_orders()
        self.assertEqual(len(all_orders), 2)  # There should be two orders
        self.assertEqual(all_orders, self.orders)

    def test_display_orders_output(self):
        """Test that display_orders prints the correct formatted output."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.finance_compiler.display_orders(self.orders)
            output = fake_out.getvalue()

            self.assertIn("Order ID", output)
            self.assertIn("Item", output)
            self.assertIn("Qty", output)
            self.assertIn("Total", output)
            self.assertIn("Buyer", output)
            self.assertIn("Seller", output)
            self.assertIn("Date", output)

            self.assertIn(self.order1.item.name, output)
            self.assertIn(self.order2.item.name, output)
            self.assertIn(self.customer.name, output)
            self.assertIn(self.supplier.name, output)


if __name__ == "__main__":
    unittest.main()
