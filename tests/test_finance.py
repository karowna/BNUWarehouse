import unittest
import io
import os
from unittest.mock import patch
from app.finance import FinanceCompiler
from app.order import Order
from app.item import Item
from app.supplier import Supplier, SupplierManager
from app.warehouse import Warehouse
from app.customer import Customer, CustomerManager

class TestFinanceCompiler(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse(name="Main Warehouse")
        self.customer_manager = CustomerManager()
        self.supplier_manager = SupplierManager()

        self.customer = self.customer_manager.create_customer(name="Alice", email="alice@example.com")
        self.supplier = self.supplier_manager.create_supplier(name="Supplier A", email="supplier@example.com")

        self.item1 = Item(name="Widget", description="A small widget", price=19.99, supplier=self.supplier)
        self.item2 = Item(name="Gadget", description="A useful gadget", price=24.99, supplier=self.supplier)

        self.order1 = Order(item=self.item1, quantity=5, buyer=self.customer, seller=self.warehouse)
        self.order1.status = "delivered"

        self.order2 = Order(item=self.item2, quantity=2, buyer=self.warehouse, seller=self.supplier)
        self.order2.status = "pending"

        self.orders = [self.order1, self.order2]
        self.finance_compiler = FinanceCompiler(self.orders)

    def test_total_customer_revenue_with_delivered_orders(self):
        """Test total revenue calculation with delivered customer orders."""
        self.order1.status = "delivered"
        self.finance_compiler.orders = [self.order1]
        expected_revenue = self.order1.total_price
        revenue = self.finance_compiler.total_customer_revenue()
        self.assertEqual(revenue, expected_revenue)

    def test_total_supplier_costs_with_received_orders(self):
        """Test total supplier cost calculation with received supplier orders."""
        self.order2.status = "received"
        self.finance_compiler.orders = [self.order2]
        expected_cost = self.order2.total_price
        cost = self.finance_compiler.total_supplier_costs()
        self.assertEqual(cost, expected_cost)


    def test_total_customer_revenue_no_delivered_orders(self):
        """Test when there are no delivered customer orders."""
        self.finance_compiler.orders = [self.order2]  # No customer orders delivered
        revenue = self.finance_compiler.total_customer_revenue()
        self.assertEqual(revenue, 0.0)

    def test_total_supplier_costs_no_received_orders(self):
        """Test when there are no received supplier orders."""
        self.finance_compiler.orders = [self.order1]  # No supplier orders received
        costs = self.finance_compiler.total_supplier_costs()
        self.assertEqual(costs, 0.0)

    def test_calculate_profit_no_customer_revenue(self):
        """Test when there is no customer revenue."""
        self.finance_compiler.orders = [self.order2]
        profit = self.finance_compiler.calculate_profit()
        self.assertEqual(profit, 0.0)

    def test_calculate_profit_no_supplier_costs(self):
        """Test when there are no supplier costs."""
        self.finance_compiler.orders = [self.order2]
        profit = self.finance_compiler.calculate_profit()
        self.assertEqual(profit, 0.0)

    def test_get_customer_orders_no_delivered(self):
        """Test when there are no customer orders with 'delivered' status."""
        self.finance_compiler.orders = [self.order2]  # No delivered customer orders
        customer_orders = self.finance_compiler.get_customer_orders()
        self.assertEqual(customer_orders, [])

    def test_get_supplier_orders_no_received(self):
        """Test when there are no supplier orders with 'received' status."""
        self.finance_compiler.orders = [self.order1]  # No received supplier orders
        supplier_orders = self.finance_compiler.get_supplier_orders()
        self.assertEqual(supplier_orders, [])

    def test_get_all_orders_no_orders(self):
        """Test when there are no orders."""
        self.finance_compiler.orders = []  # No orders
        all_orders = self.finance_compiler.get_all_orders()
        self.assertEqual(all_orders, [])

    def test_summarise_orders(self):
        summary = self.finance_compiler.summarise_orders()
        self.assertEqual(len(summary), 2)
        self.assertIn("order_id", summary[0])
        self.assertIn("total_price", summary[0])
        self.assertIn("item_name", summary[0])

    def test_summarise_orders_no_orders(self):
        """Test that summarise_orders returns an empty list and prints a message when there are no orders."""
        self.finance_compiler.orders = []

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            summary = self.finance_compiler.summarise_orders()
            output = fake_out.getvalue()

            self.assertEqual(summary, [])
            self.assertIn("No orders found.", output)


    def test_display_orders_output(self):
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

    def test_export_orders_to_csv(self):
        file_path = "test_orders.csv"
        self.finance_compiler.export_orders_to_csv(self.orders, file_path)
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.assertGreater(len(lines), 1)
        finally:
            os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
