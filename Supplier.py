class Supplier(Person):
    _id_counter = 1
    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email)
        self.items_supplied = []

    @property
    def supplier_id(self):
        return self.person_id

    @classmethod
    def create(cls, name, email):
        person_id = cls._id_counter
        cls._id_counter += 1
        return cls(name, email, person_id)
