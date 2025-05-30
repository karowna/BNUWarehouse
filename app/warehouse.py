from typing import List, Dict
from app.inventory import Inventory
from app.customer import Customer
from app.order import Order
from app.item import Item

class Warehouse:
    def __init__(self, name: str):
        self.name = name
        self.suppliers: List['Supplier'] = []
        self.inventory = Inventory()
        self.orders: List[Order] = []

    def view_inventory(self):
        inventory = self.inventory.get_all_items()
        if not inventory:
            print("No items in inventory.")
            return {}

        return inventory

    def mark_order_as_received(self, order_id: int):
        """Marks an order as 'received' and adds stock to inventory."""
        order = next((order for order in self.orders if order.order_id == order_id), None)
        
        if not order:
            print(f"Order with ID {order_id} not found.")
            return
        
        if order.status == "received":
            print(f"Order #{order_id} has already been marked as received.")
            return
        
        order.status = "received"
        
        # Add stock to inventory now
        self.inventory.add_stock(order.item, order.quantity)
        print(f"Order #{order_id} marked as received and stock updated.")

    def list_pending_orders(self):
        """Returns a list of all pending orders."""
        return [order for order in self.orders if order.status != "received"]

    def get_available_items(self) -> Dict[Item, int]:
        """Returns items that are above the threshold and marked as 'received', with error handling."""
        available_items = {}

        for item, (quantity, threshold) in self.inventory.get_full_item_info().items():
            try:
                if quantity > threshold and any(order.item == item and order.status == "received" for order in self.orders):
                    available_items[item] = quantity
            except Exception as e:
                print(f"Error processing item '{item.name}': {e}")
                continue

        # Check if no items are available
        if not available_items:
            print("No items are currently available for purchase.")
        
        return available_items


    def _record_transaction(self, item: Item, quantity: int, buyer, seller) -> Order:
        order = Order(item=item, quantity=quantity, buyer=buyer, seller=seller)
        self.orders.append(order)

        if isinstance(buyer, Customer):
            buyer.order_history.append(order)

        return order

    def place_order(self, customer: Customer, item: Item, quantity: int) -> Order:
        """Customer places an order from the warehouse inventory, default status 'delivered'."""
        if self.inventory.check_stock(item) < quantity:
            raise ValueError("Not enough stock.")

        self.inventory.remove_stock(item, quantity)
        order = Order(item=item, quantity=quantity, buyer=customer, seller=self, status="delivered")
        self.orders.append(order)

        if isinstance(customer, Customer):
            customer.order_history.append(order)

        return order


    def order_from_supplier(self, supplier, item: Item, quantity: int) -> Order:
        """Warehouse orders stock from a supplier. Raises if supplier has no items."""
        if not supplier.items_supplied:
            raise ValueError(f"{supplier.name} has no items available.")
        order = self._record_transaction(item, quantity, buyer=self, seller=supplier)
        return order

