class Item:
    def __init__(self, name: str, description: str, price: float, supplier=None):
        self.name = name
        self.description = description
        self.price = price
        self.supplier = supplier  # Optional

    def __str__(self):
        return f"{self.name} - {self.description} (£{self.price:.2f})"

    def __repr__(self):
        return f"Item({self.name})"

    def __hash__(self):
        # Only use immutable fields for hashing
        return hash((self.name, self.description))

    def __eq__(self, other):
        return isinstance(other, Item) and (
            self.name, self.description
        ) == (other.name, other.description)

    def clone(self):
        """Create a copy of the item without shared references."""
        return Item(self.name, self.description, self.price, self.supplier)

    def get_details(self) -> str:
        supplier_info = f" (Supplier: {self.supplier.name})" if self.supplier else ""
        return f"{self.name}: {self.description} - £{self.price:.2f}{supplier_info}"
