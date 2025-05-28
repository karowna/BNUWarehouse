class Item:
    def __init__(self, name: str, description: str, price: float, supplier):
        self.name = name
        self.description = description
        self.price = price
        self.supplier = supplier

    def get_details(self) -> str:
        return f"{self.name}: {self.description} - ${self.price:.2f} (Supplier: {self.supplier})"

    def __repr__(self):
        return f"Item({self.name})"
