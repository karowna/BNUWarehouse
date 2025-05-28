from typing import List
from app.inventory import Inventory
from app.order import Order

class Warehouse:
    def __init__(self):
        self.suppliers: List['Supplier'] = []
        self.inventory = Inventory()
        
        self.orders: List[Order] = []

    def view_inventory(self) -> dict:
        return self.inventory.get_all_stock()

    def get_available_stock(self) -> dict:
        return self.inventory.get_all_stock()

    def process_order(self, order: Order) -> None:
        self.inventory.remove_stock(order.item, order.quantity)
        self.orders.append(order)

    def get_all_orders(self) -> List[Order]:
        return list(self.orders)

    def _record_transaction(self, item, quantity, buyer, seller):
        order = Order(item=item, quantity=quantity, buyer=buyer, seller=seller)
        self.orders.append(order)
        if isinstance(buyer, Customer):
            buyer.orders.append(order)
        return order

    def place_order(self, customer, item, quantity):
        if self.inventory.check_stock(item) < quantity:
            raise ValueError("Not enough stock.")
        self.inventory.remove_stock(item, quantity)
        return self._record_transaction(item, quantity, buyer=customer, seller=self)

    def order_from_supplier(self, supplier, item, quantity):
        self.inventory.add_stock(item, quantity)
        return self._record_transaction(item, quantity, buyer=self, seller=supplier)



