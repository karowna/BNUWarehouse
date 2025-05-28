from typing import Dict, List
from app.item import Item

class Inventory:
    def __init__(self):
        self.stock: Dict[Item, int] = {}

    def add_stock(self, item: Item, quantity: int) -> None:
        self.stock[item] = self.stock.get(item, 0) + quantity

    def remove_stock(self, item: Item, quantity: int) -> None:
        if item in self.stock and self.stock[item] >= quantity:
            self.stock[item] -= quantity
            if self.stock[item] == 0:
                del self.stock[item]
        else:
            raise ValueError("Insufficient stock")

    def check_stock(self, item: Item) -> int:
        return self.stock.get(item, 0)

    def low_stock_alerts(self, threshold: int = 5) -> List[Item]:
        return [item for item, qty in self.stock.items() if qty < threshold]

    def get_all_stock(self) -> Dict[Item, int]:
        return dict(self.stock)
