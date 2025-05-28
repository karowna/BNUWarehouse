from typing import List
from inventory import Inventory
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
