from typing import Dict, List, Tuple
from app.item import Item

class Inventory:
    def __init__(self):
        self.stock: Dict[Item, Tuple[int, int]] = {}

    def add_stock(self, item: Item, quantity: int, threshold: int = None) -> None:
        item_copy = item.clone()  # Ensure local copy
        if item_copy in self.stock:
            current_qty, current_threshold = self.stock[item_copy]
            new_threshold = threshold if threshold is not None else current_threshold
            self.stock[item_copy] = (current_qty + quantity, new_threshold)
        else:
            self.stock[item_copy] = (quantity, threshold if threshold is not None else 0)

    def remove_stock(self, item: Item, quantity: int) -> None:
        if item not in self.stock:
            raise ValueError("Item not found in inventory.")

        current_quantity, threshold = self.stock[item]
        if quantity > current_quantity:
            raise ValueError("Not enough stock available.")

        self.stock[item] = (current_quantity - quantity, threshold)

    def check_stock(self, item: Item) -> int:
        return self.stock.get(item, (0, 0))[0]

    def set_threshold(self, item: Item, threshold: int) -> None:
        if item in self.stock:
            quantity, _ = self.stock[item]
            self.stock[item] = (quantity, threshold)
        else:
            raise ValueError("Item not found in inventory")

    def update_price(self, item_name: str, new_price: float) -> None:
        for item in self.stock.keys():
            if item.name == item_name:
                item.price = new_price
                return
        raise ValueError(f"Item '{item_name}' not found in inventory.")

    def low_stock_alerts(self) -> List[Item]:
        return [item for item, (qty, threshold) in self.stock.items() if qty < threshold]

    def get_all_items(self) -> Dict[Item, int]:
        return {item: qty for item, (qty, _) in self.stock.items()}

    def get_full_item_info(self) -> Dict[Item, Tuple[int, int]]:
        return dict(self.stock)
