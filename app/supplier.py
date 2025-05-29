from app.person import Person
from app.item import Item

class Supplier(Person):
    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email)
        self.items_supplied = []

    def get_role(self):
        return "Supplier"

    @property
    def supplier_id(self):
        return self.person_id

    def update_profile(self, name=None, email=None):  # Supplier can be responsible for their own internal state, but not for creating more suppliers, hence SupplierManager
        if name:
            self.name = name
        if email:
            self.email = email

    def add_item(self, item):
        self.items_supplied.append(item)

    def remove_item(self, item):
        if item in self.items_supplied:
            self.items_supplied.remove(item)
        else:
            print(f"Item {item.name} not found in the list.")

class SupplierManager:
    def __init__(self):
        self.suppliers = {}

    def get_all_suppliers(self):
        """Return a list of all suppliers."""
        return list(self.suppliers.values())

    def create_supplier(self, name, email, person_id):
        if person_id in self.suppliers:
            raise ValueError(f"Supplier with ID {person_id} already exists.")
        supplier = Supplier(name, email, person_id)
        self.suppliers[supplier.supplier_id] = supplier
        return supplier

    def get_supplier_by_id(self, supplier_id):
        return self.suppliers.get(supplier_id)

    def get_supplier_items(self, supplier_id):
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            return supplier.items_supplied
        return []

    def create_supplier_item(self, supplier_id, name=None, description=None, price=None, item=None):
        supplier = self.get_supplier_by_id(supplier_id)
        if not supplier:
            raise ValueError(f"No supplier found with ID {supplier_id}")
        
        # Check if the item already exists
        for existing_item in supplier.items_supplied:
            if existing_item.name == name and existing_item.description == description:
                raise ValueError(f"Item '{name}' with description '{description}' already exists.")

        if item is None:
            if None in (name, description, price):
                raise ValueError("To create a new item, name, description, and price must be provided.")
            item = Item(name, description, price, supplier)

        supplier.add_item(item)
        return item

    def remove_item_from_supplier(self, supplier_id, item):
        supplier = self.get_supplier_by_id(supplier_id)
        if supplier:
            supplier.remove_item(item)
        else:
            raise ValueError(f"Supplier with ID {supplier_id} not found.")
