class Supplier(Person):

    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email) # Using the Person constructor via Super
        self.items_supplied = []

    @property # Property to alias the person_id as supplier_id to make things more readable
    def supplier_id(self):
        return self.person_id

class SupplierManager: # Manages supplier objects, supplier should not manage itself
    pass