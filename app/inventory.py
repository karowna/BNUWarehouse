from typing import Dict, List, Tuple
from app.item import Item

class Inventory:
    def __init__(self):
        # Each item maps to a tuple: (quantity, threshold)
        self.stock: Dict[Item, Tuple[int, int]] = {}

    def add_stock(self, item: Item, quantity: int, threshold: int = None) -> None:
        if item in self.stock:
            current_qty, current_threshold = self.stock[item]
            new_threshold = threshold if threshold is not None else current_threshold
            self.stock[item] = (current_qty + quantity, new_threshold)
        else:
            self.stock[item] = (quantity, threshold if threshold is not None else 0) # Default threshold is 0 if not specified

    def check_stock(self, item: Item) -> int:
        return self.stock.get(item, (0, 0))[0]

    def set_threshold(self, item: Item, threshold: int) -> None:
        if item in self.stock:
            quantity, _ = self.stock[item]
            self.stock[item] = (quantity, threshold)
        else:
            raise ValueError("Item not found in inventory")

    def low_stock_alerts(self) -> List[Item]:
        return [item for item, (qty, threshold) in self.stock.items() if qty < threshold]

    def get_all_stock(self) -> Dict[Item, int]:
        return {item: qty for item, (qty, _) in self.stock.items()}

    def get_full_stock_info(self) -> Dict[Item, Tuple[int, int]]:
        return dict(self.stock)
