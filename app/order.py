from typing import Union
from datetime import datetime
from app.item import Item

class Order:
    def __init__(self, item: Item, quantity: int, buyer: Union['Customer', 'Warehouse'], seller: Union['Warehouse', 'Supplier']):
        self.item = item
        self.quantity = quantity
        self.timestamp = datetime.now()
        self.buyer = buyer
        self.seller = seller
        self.total_price = item.price * quantity

    def generate_invoice(self) -> str:
        return (
            f"Invoice:\n"
            f"Item: {self.item.name}\n"
            f"Quantity: {self.quantity}\n"
            f"Total Price: £{self.total_price:.2f}\n"
            f"Buyer: {self.buyer}\n"
            f"Seller: {self.seller}\n"
            f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def __repr__(self):
        return f"Order({self.item.name}, Qty: {self.quantity}, Buyer: {self.buyer})"
