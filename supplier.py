from person import Person

class Supplier(Person):

    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email) # Using the Person constructor via Super
        self.items_supplied = []

    def get_role(self):
        return "Supplier"

    @property # Property to alias the person_id as supplier_id to make things more readable
    def supplier_id(self):
        return self.person_id
    
class SupplierManager:
    def __init__(self):
        self.suppliers = {}

    def create_supplier(self, name, email, person_id):
        if person_id in self.suppliers:
            raise ValueError(f"Supplier with ID {person_id} already exists.")
        supplier = Supplier(name, email, person_id)
        self.suppliers[supplier.supplier_id] = supplier
        return supplier

    def get_supplier_by_id(self, supplier_id):
        return self.suppliers.get(supplier_id)

    def update_supplier(self, supplier_id, **kwargs):
        supplier = self.get_supplier_by_id(supplier_id)
        if not supplier:
            raise ValueError(f"No supplier found with ID {supplier_id}")
        for key, value in kwargs.items():
            if hasattr(supplier, key):
                setattr(supplier, key, value)

    def delete_supplier(self, supplier_id):
        if supplier_id in self.suppliers:
            del self.suppliers[supplier_id]
        else:
            raise ValueError(f"No supplier found with ID {supplier_id}")

