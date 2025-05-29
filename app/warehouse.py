from typing import List
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

    def view_inventory(self) -> dict:
        return self.inventory.get_all_items()

    def get_items_above_threshold(self):
        stock_info = self.inventory.get_full_item_info()
        return {item: qty_thresh for item, qty_thresh in stock_info.items() if qty_thresh[0] > qty_thresh[1]}

    def _record_transaction(self, item: Item, quantity: int, buyer, seller) -> Order:
        order = Order(item=item, quantity=quantity, buyer=buyer, seller=seller)
        self.orders.append(order)

        if isinstance(buyer, Customer):
            buyer.order_history.append(order)

        return order

    def place_order(self, customer: Customer, item: Item, quantity: int) -> Order:
        """ Customer places an order from the warehouse. """
        if self.inventory.check_stock(item) < quantity:
            raise ValueError("Not enough stock.")

        self.inventory.remove_stock(item, quantity)
        return self._record_transaction(item, quantity, buyer=customer, seller=self)

    def order_from_supplier(self, supplier, item: Item, quantity: int) -> Order:
        """ Warehouse orders stock from a supplier. """
        self.inventory.add_stock(item, quantity)
        order = self._record_transaction(item, quantity, buyer=self, seller=supplier)
        return order
