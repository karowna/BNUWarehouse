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

        # Give the supplier some items
        self.supplier_manager.create_supplier_item(
            supplier_id=self.supplier.supplier_id,
            name="Widget",
            description="A small widget",
            price=19.99
        )
        self.supplier_manager.create_supplier_item(
            supplier_id=self.supplier.supplier_id,
            name="Gadget",
            description="A useful gadget",
            price=29.99
        )

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

    def test_get_available_items(self):
        """Test that items above their threshold are returned correctly."""

        # Define threshold and quantity
        threshold = 5
        quantity = 10

        # Add stock to warehouse inventory
        self.warehouse.inventory.add_stock(self.item, quantity, threshold=threshold)

        # Simulate a customer order that has been marked as received
        order = Order(item=self.item, quantity=quantity, buyer=self.customer, seller=self.warehouse, status="received")
        self.warehouse.orders.append(order)

        # Call the method under test
        available_items = self.warehouse.get_available_items()

        # Verify that the item appears in the available items with the correct quantity
        self.assertIn(self.item, available_items)
        self.assertEqual(available_items[self.item], 20) # 10 (initial) + 10 (added) = 20

    def test_place_order_insufficient_stock(self):
        """Test the behavior when there's not enough stock for an order."""
        # Attempt to order 15 items when only 10 are in stock
        with self.assertRaises(ValueError):
            self.warehouse.place_order(self.customer, self.cloned_item, 15)

    def test_order_from_supplier(self):
        """Test the warehouse ordering items from a supplier."""
        # Order 10 items from the supplier
        order = self.warehouse.order_from_supplier(self.supplier, self.cloned_item, 10)
        self.warehouse.mark_order_as_received(order.order_id)

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

    def test_update_price_item_not_found(self):
        """Test that updating price raises ValueError when item is not found."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.update_price("Nonexistent Item", 19.99)
        self.assertEqual(str(context.exception), "Item 'Nonexistent Item' not found in inventory.")

    def test_set_threshold_item_found(self):
        """Test setting threshold for an item that exists in stock."""
        # Set a new threshold for an item in the inventory
        self.warehouse.inventory.set_threshold(self.item.name, 10)
        
        # Get the updated stock information
        stock_info = self.warehouse.inventory.get_full_item_info()
        
        # Assert that the threshold for the item has been updated
        self.assertEqual(stock_info[self.cloned_item][1], 10)  # Threshold should be 10

    def test_set_threshold_item_not_found(self):
        """Test setting threshold for an item that does not exist in inventory."""
        with self.assertRaises(ValueError) as context:
            self.warehouse.inventory.set_threshold(self.non_existent_item.name, 5)
        self.assertEqual(str(context.exception), "Item 'Nonexistent' not found in inventory.")

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

    def test_low_stock_alerts_empty_inventory(self):
        """Test that low_stock_alerts returns an empty list when inventory is empty."""
        empty_inventory = Inventory()
        alerts = empty_inventory.low_stock_alerts()
        self.assertEqual(alerts, [])

    def test_low_stock_alerts_all_healthy(self):
        """Test that low_stock_alerts returns an empty list when all stock levels are above threshold."""
        inventory = Inventory()
        inventory.add_stock(self.item, 10, threshold=5)  # Healthy stock
        alerts = inventory.low_stock_alerts()
        self.assertEqual(alerts, [])

    def test_get_all_items_empty_inventory(self):
        """Test that get_all_items returns an empty dictionary when inventory is empty."""
        empty_inventory = Inventory()
        items = empty_inventory.get_all_items()
        self.assertEqual(items, {})


    def test_get_all_items_with_inventory(self):
        """Test that get_all_items returns the correct dictionary when inventory has items."""
        inventory = Inventory()
        inventory.add_stock(self.item, 10, threshold=5)

        # Extract the actual item key from inventory (since it's a clone)
        item_key = next(iter(inventory.stock.keys()))
        expected = {item_key: (10, 5)}

        result = inventory.get_all_items()
        self.assertEqual(result, expected)

    def test_view_inventory(self):
        """Test the view_inventory method to ensure it returns the correct inventory."""
        inventory = self.warehouse.view_inventory()
        
        # Check if the inventory has the item
        self.assertIn(self.cloned_item, inventory)
        self.assertEqual(inventory[self.cloned_item][0], 10)  # Check stock quantity
    
    def test_list_pending_orders(self):
        """Test listing pending orders."""
        order1 = self.warehouse.place_order(self.customer, self.item, 5)
        # Ensure there's enough stock for item2
        self.warehouse.inventory.add_stock(self.item2, 20, threshold=10)
        order2 = self.warehouse.place_order(self.customer, self.item2, 3)

        # Mark the first order as received
        self.warehouse.mark_order_as_received(order1.order_id)

        # List pending orders, should only include order2
        pending_orders = self.warehouse.list_pending_orders()
        self.assertEqual(len(pending_orders), 1)
        self.assertEqual(pending_orders[0].order_id, order2.order_id)


    def test_get_available_items(self):
        """Test that available items above threshold are returned correctly."""
        # Add stock to warehouse inventory above threshold
        self.warehouse.inventory.add_stock(self.item, 10, threshold=5)
        
        # Simulate a customer order that has been marked as received
        order = Order(item=self.item, quantity=10, buyer=self.customer, seller=self.warehouse, status="received")
        self.warehouse.orders.append(order)

        # Call the method under test
        available_items = self.warehouse.get_available_items()

        # Verify that the item appears in the available items with the correct quantity
        self.assertIn(self.item, available_items)
        self.assertEqual(available_items[self.item], 20)  # 10 initial + 10 added

    def test_get_available_items_below_threshold(self):
        """Test that items below threshold are not returned as available."""
        self.warehouse.inventory.add_stock(self.item2, 5, threshold=10)

        # Simulate a customer order that has been marked as received
        order = Order(item=self.item2, quantity=5, buyer=self.customer, seller=self.warehouse, status="received")
        self.warehouse.orders.append(order)

        # Call the method under test
        available_items = self.warehouse.get_available_items()

        # Verify that the item does not appear in the available items
        self.assertNotIn(self.item2, available_items)

    def test_place_order_success(self):
        """Test that placing an order successfully deducts stock."""
        order = self.warehouse.place_order(self.customer, self.item, 5)
        
        # Verify that the order is in the customer's order history
        self.assertIn(order, self.customer.order_history)
        self.assertEqual(len(self.customer.order_history), 1)  # The customer should have one order
        
        # Verify the stock level after placing the order
        self.assertEqual(self.warehouse.inventory.check_stock(self.cloned_item), 5)

    def test_place_order_insufficient_stock(self):
        """Test placing an order with insufficient stock."""
        with self.assertRaises(ValueError):
            self.warehouse.place_order(self.customer, self.item, 15)  # More than available stock

    def test_order_from_supplier_success(self):
        """Test ordering items from a supplier."""
        order = self.warehouse.order_from_supplier(self.supplier, self.cloned_item, 10)
        self.warehouse.mark_order_as_received(order.order_id)
        
        # Verify the stock level after receiving the order
        self.assertEqual(self.warehouse.inventory.check_stock(self.cloned_item), 20)

    def test_order_from_supplier_invalid_quantity(self):
        """Test ordering items from a supplier with invalid quantity."""
        with self.assertRaises(ValueError):
            self.warehouse.order_from_supplier(self.supplier, self.cloned_item, -5)  # Invalid quantity

    def test_order_from_supplier_no_items_available(self):
        """Test ordering items from a supplier with no available items."""
        new_supplier = self.supplier_manager.create_supplier(name="Supplier B", email="supplierb@example.com")
        with self.assertRaises(ValueError):
            self.warehouse.order_from_supplier(new_supplier, self.cloned_item, 5)  # No items available
            

if __name__ == "__main__":
    unittest.main()
