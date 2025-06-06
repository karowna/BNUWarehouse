# /app/supplier.py

from app.person import Person
from app.item import Item


class Supplier(Person):
    _supplier_counter = 1  # Class-level counter to keep track of created suppliers

    def __init__(self, name, email):
        super().__init__(name, email)  # Using the Person constructor via Super
        self.person_id = self.generate_id()  # Automatically assign a unique ID
        self.items_supplied = []  # Initialize the list of items supplied

    def get_role(self):
        return "Supplier"

    def generate_id(self):
        """Generate a unique supplier ID."""
        supplier_id = f"su_{Supplier._supplier_counter}"
        Supplier._supplier_counter += 1  # Increment the counter for the next supplier
        return supplier_id

    @property
    def supplier_id(self):
        return self.person_id

    def add_item(self, item):
        """Add an item to the supplier's list."""
        self.items_supplied.append(item)

    def remove_item(self, item):
        """Remove an item from the supplier's list."""
        if item in self.items_supplied:
            self.items_supplied.remove(item)
        else:
            print(f"Item {item.name} not found in the list.")


class SupplierManager:
    def __init__(self):
        self.suppliers = {}

    def get_all_suppliers(self):
        """Return a list of all suppliers, or raise an error if none exist."""
        if not self.suppliers:
            raise ValueError("No suppliers available.")
        return list(self.suppliers.values())

    def create_supplier(self, name, email):
        """Create a new supplier and assign them a unique ID."""
        supplier = Supplier(name, email)
        self.suppliers[supplier.supplier_id] = supplier
        return supplier

    def get_supplier_by_id(self, supplier_id):
        """Retrieve a supplier by their ID."""
        if not self.suppliers:
            print("No suppliers available.")
            return None

        if supplier_id not in self.suppliers:
            print(f"supplier with ID {supplier_id} not found.")
            return None

        return self.suppliers[supplier_id]

    def get_supplier_items(self, supplier_id):
        """Retrieve all items supplied by a given supplier."""
        supplier = self.get_supplier_by_id(supplier_id)

        if not supplier:
            raise ValueError(f"Supplier with ID {supplier_id} not found.")

        if not supplier.items_supplied:
            raise ValueError(f"No items found for supplier with ID {supplier_id}.")

        return supplier.items_supplied

    def create_supplier_item(
        self, supplier_id, name=None, description=None, price=None, item=None
    ):
        """Create a new item for the given supplier."""
        supplier = self.get_supplier_by_id(supplier_id)
        if not supplier:
            raise ValueError(f"No supplier found with ID {supplier_id}")

        if any(
            existing_item.name == name and existing_item.description == description
            for existing_item in supplier.items_supplied
        ):
            raise ValueError(
                f"Item '{name}' with description '{description}' already exists."
            )

        if item is None:
            if None in (name, description, price):
                raise ValueError(
                    "To create a new item, name, description, and price must be provided."
                )
            item = Item(name, description, price, supplier)
        supplier.add_item(item)
        return item

    def remove_item_from_supplier(self, supplier_id, item):
        """Remove an item from the supplier's inventory."""
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            supplier.remove_item(item)
        else:
            raise ValueError(f"Supplier with ID {supplier_id} not found.")
