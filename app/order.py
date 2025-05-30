from typing import Union
from datetime import datetime
from app.item import Item

class Order:
    _id_counter = 1

    def __init__(self, item: Item, quantity: int, buyer: Union['Customer', 'Warehouse'], seller: Union['Warehouse', 'Supplier']):
        self.order_id = Order._id_counter
        Order._id_counter += 1

        self.item = item
        self.quantity = quantity
        self.timestamp = datetime.now()
        self.buyer = buyer
        self.seller = seller
        self.total_price = item.price * quantity
        self.status = "pending"  # Default status is 'pending'

    def __repr__(self):
        return f"Order #{self.order_id} ({self.item.name}, Qty: {self.quantity}, Buyer: {getattr(self.buyer, 'name', 'Warehouse')}, Status: {self.status})"
