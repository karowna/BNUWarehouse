class Customer(Person):
    _id_counter = 1

    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email)
        self.order_history = []

    @property
    def customer_id(self):
        return self.person_id

    @classmethod
    def create(cls, name, email):
        person_id = cls._id_counter
        cls._id_counter += 1
        return cls(name, email, person_id)

    def view_order_history(self):
        return self.order_history
