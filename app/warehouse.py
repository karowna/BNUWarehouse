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
        return self.inventory.get_all_stock()

    def get_available_stock(self) -> dict:
        return self.inventory.get_all_stock()

    def process_order(self, order: Order) -> None:
        self.inventory.remove_stock(order.item, order.quantity)
        self.orders.append(order)

    def _summarise_order(self, order) -> dict:
        return {
            "order_id": order.order_id,
            "item_name": order.item.name,
            "item_description": order.item.description,
            "item_price": order.item.price,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "buyer_name": getattr(order.buyer, 'name', 'N/A'),
            "seller_name": getattr(order.seller, 'name', 'N/A'),
            "timestamp": order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def summarise_orders(self) -> list[dict]:
        return [self._summarise_order(order) for order in self.orders]

    def summarise_my_orders(self) -> list[dict]:
        return [self._summarise_order(order) for order in self.get_my_orders()]

    def summarise_customer_orders(self) -> list[dict]:
        return [self._summarise_order(order) for order in self.get_customer_orders()]

    def get_my_orders(self) -> List[Order]:
        return [order for order in self.orders if order.buyer == self]

    def get_customer_orders(self) -> List[Order]:
        return [order for order in self.orders if isinstance(order.buyer, Customer)]

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

    def order_from_supplier(self, supplier, item, quantity):
        item_for_inventory = Item(item.name, item.description, item.price)
        self.inventory.add_stock(item_for_inventory, quantity)
        return self._record_transaction(item_for_inventory, quantity, buyer=self, seller=supplier)
