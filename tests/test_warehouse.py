import unittest
from app.inventory import Inventory
from app.item import Item
from app.customer import Customer, CustomerManager
from app.warehouse import Warehouse
from app.supplier import Supplier, SupplierManager
from app.order import Order

class TestWarehouse(unittest.TestCase):

    def setUp(self):
        # Create a warehouse instance
        self.warehouse = Warehouse(name="Main Warehouse")

        # Create a customer and supplier using their respective manager classes
        self.customer_manager = CustomerManager()
        self.supplier_manager = SupplierManager()

        # Create mock customer and supplier
        self.customer = self.customer_manager.create_customer(name="Alice", email="alice@example.com")
        self.supplier = self.supplier_manager.create_supplier(name="Supplier A", email="supplier@example.com")

        # Create item instances for testing
        self.item = Item(name="Widget", description="A small widget", price=19.99, supplier=self.supplier)
        self.item2 = Item(name="Gadget", description="A small gadget", price=29.99, supplier=self.supplier)  # Add a second item

        # Add item to warehouse inventory using add_stock
        self.warehouse.inventory.add_stock(self.item, 10, threshold=5)

        # Get the cloned version of the item in the stock
        self.cloned_item = next(iter(self.warehouse.inventory.stock.keys()))  # Get the first (and only) cloned item

        # Create an item that isn't in the inventory (to test error cases)
        self.non_existent_item = Item(name="Nonexistent", description="An item not in the inventory", price=99.99, supplier=self.supplier)

    def test_inventory_add_stock_with_threshold(self):
        """Test adding stock with a custom threshold."""
        # Add more stock with a custom threshold
        self.warehouse.inventory.add_stock(self.item, 5, threshold=3)
        
        # Get the updated stock information for the cloned item
        stock_info = self.warehouse.inventory.get_full_item_info()
        
        # Assert stock and threshold values for the cloned item
        self.assertEqual(stock_info[self.cloned_item][0], 15)  # 10 (initial) + 5 (added) = 15
        self.assertEqual(stock_info[self.cloned_item][1], 3)   # Threshold should be 3

    def test_inventory_update_price(self):
        """Test updating the price of an item in the warehouse inventory."""
        # Update the price of the cloned item in the inventory
        self.warehouse.inventory.update_price(self.cloned_item.name, 24.99)

        # Assert that the price of the cloned item has been updated
        self.assertEqual(self.cloned_item.price, 24.99)

    def test_get_items_above_threshold(self):
        """Test retrieval of items above their stock threshold."""
        # Add stock with a threshold of 5
        self.warehouse.inventory.add_stock(self.item, 3, threshold=5)  # Stock is 3, threshold is 5

        # Get the items above threshold
        items_above_threshold = self.warehouse.get_items_above_threshold()
        
        # Assert that the cloned item is in the list of items above the threshold
        self.assertIn(self.cloned_item, items_above_threshold)

    def test_view_inventory_empty(self):
        """Test that an empty inventory shows an empty dictionary."""
        empty_warehouse = Warehouse(name="Empty Warehouse")
        self.assertEqual(empty_warehouse.view_inventory(), {})

    def test_place_order_insufficient_stock(self):
        """Test the behavior when there's not enough stock for an order."""
        # Attempt to order 15 items when only 10 are in stock
        with self.assertRaises(ValueError):
            self.warehouse.place_order(self.customer, self.cloned_item, 15)

    def test_order_from_supplier(self):
        """Test the warehouse ordering items from a supplier."""
        # Order 10 items from the supplier
        order = self.warehouse.order_from_supplier(self.supplier, self.cloned_item, 10)
        
        # Assert the order details
        self.assertEqual(order.buyer, self.warehouse)
        self.assertEqual(order.seller, self.supplier)

        # Check if the stock has increased
        self.assertEqual(self.warehouse.inventory.check_stock(self.cloned_item), 20)  # Stock should increase by 10

    def test_place_order_success(self):
        """Test the customer placing an order successfully."""
        order = self.warehouse.place_order(self.customer, self.item, 5)
        
        # Verify that the order is in the customer's order history
        self.assertIn(order, self.customer.order_history)
        self.assertEqual(len(self.customer.order_history), 1)  # The customer should have one order

    def test_remove_stock_item_not_found(self):
        """Test that removing stock raises ValueError when item is not found."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.remove_stock(self.non_existent_item, 1)  # Use the non-existent item
        self.assertEqual(str(context.exception), "Item not found in inventory.")

    def test_set_threshold_item_not_found(self):
        """Test that setting threshold raises ValueError when item is not found."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.set_threshold(self.non_existent_item, 5)  # Use the non-existent item
        self.assertEqual(str(context.exception), "Item not found in inventory")

    def test_update_price_item_not_found(self):
        """Test that updating price raises ValueError when item is not found."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.update_price("Nonexistent Item", 19.99)
        self.assertEqual(str(context.exception), "Item 'Nonexistent Item' not found in inventory.")

    def test_set_threshold_item_found(self):
        """Test setting threshold for an item that exists in stock."""
        # Set a new threshold for an item in the inventory
        self.warehouse.inventory.set_threshold(self.item, 10)
        
        # Get the updated stock information
        stock_info = self.warehouse.inventory.get_full_item_info()
        
        # Assert that the threshold for the item has been updated
        self.assertEqual(stock_info[self.cloned_item][1], 10)  # Threshold should be 10

    def test_set_threshold_item_not_found(self):
        """Test setting threshold for an item that does not exist in inventory."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.set_threshold(self.non_existent_item, 5)
        self.assertEqual(str(context.exception), "Item not found in inventory")

    def test_remove_stock_not_enough_available(self):
        """Test that removing more stock than available raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.remove_stock(self.item, 20)  # Attempt to remove 20 items when only 10 are in stock
        self.assertEqual(str(context.exception), "Not enough stock available.")

    def test_low_stock_alerts(self):
        """Test that low stock alerts return items below their threshold."""
        # Add an item with a low stock
        self.warehouse.inventory.add_stock(self.item2, 2, threshold=5)
        low_stock_items = self.warehouse.inventory.low_stock_alerts()
        self.assertIn(self.item2, low_stock_items)
        self.assertEqual(len(low_stock_items), 1)
        
if __name__ == "__main__":
    unittest.main()
