# app/customer.py
from app.person import Person

class Customer(Person):
    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email) # Using the Person constructor via Super
        self.order_history: List[Order] = []

    def get_role(self):
        return "Customer"

    @property
    def customer_id(self):
        return self.person_id

    def view_order_history(self):
        return self.order_history

    def add_order(self, order):
        """Add an order to the customer's order history."""
        self.order_history.append(order)

    def update_profile(self, name=None, email=None):
        """Allow the customer to update their own profile."""
        if name:
            self.name = name
        if email:
            self.email = email


class CustomerManager:
    def __init__(self):
        self.customers = {}

    def create_customer(self, name, email, person_id):
        """Create a new customer and store it."""
        if person_id in self.customers:
            raise ValueError(f"Customer with ID {person_id} already exists.")
        customer = Customer(name, email, person_id)
        self.customers[customer.customer_id] = customer
        return customer

    def get_customer_by_id(self, customer_id):
        """Retrieve a customer by their ID."""
        return self.customers.get(customer_id)

    def delete_customer(self, customer_id):
        """Delete a customer by their ID."""
        if customer_id in self.customers:
            del self.customers[customer_id]
        else:
            raise ValueError(f"No customer found with ID {customer_id}")
