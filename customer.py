from person import Person

class Customer(Person):

    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email) # Using the Person constructor via Super
        self.order_history = [] 

    def get_role(self):
        return "Customer"

    @property # Property to alias the person_id as customer_id to make things more readable
    def customer_id(self):
        return self.person_id

    def view_order_history(self):
        return self.order_history

class CustomerManager: # Manages customer objects, customer should not manage itself (SRP)
    def __init__(self):
        self.customers = {}

    def create_customer(self, name, email, person_id):
        if person_id in self.customers:
            raise ValueError(f"Customer with ID {person_id} already exists.")
        customer = Customer(name, email, person_id)
        self.customers[customer.customer_id] = customer
        return customer

    def get_customer_by_id(self, customer_id):
        return self.customers.get(customer_id)

    def update_customer(self, customer_id, **kwargs):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"No customer found with ID {customer_id}")
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            del self.customers[customer_id]
        else:
            raise ValueError(f"No customer found with ID {customer_id}")
