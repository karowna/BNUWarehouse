# /app/customer.py

from app.person import Person


class Customer(Person):
    _customer_counter = 1  # Class-level counter to keep track of created customers

    def __init__(self, name, email):
        super().__init__(name, email)  # Using the Person constructor via Super
        self.person_id = self.generate_id()  # Automatically assign a unique ID
        self.order_history = []  # Initialize the order history as an empty list

    def get_role(self):
        return "Customer"

    def generate_id(self):
        """Generate a unique customer ID."""
        customer_id = f"cu_{Customer._customer_counter}"
        Customer._customer_counter += 1  # Increment the counter for next customer
        return customer_id

    @property
    def customer_id(self):
        return self.person_id

    def view_order_history(self):
        """Return the customer's order history if it exists."""
        if not self.order_history:
            print("No order history available")
            return None
        return self.order_history

    def add_order(self, order):
        """Add an order to the customer's order history."""
        self.order_history.append(order)


class CustomerManager:
    def __init__(self):
        self.customers = {}

    def create_customer(self, name, email):
        """Create a new customer and store it."""
        customer = Customer(name, email)
        self.customers[customer.customer_id] = customer
        return customer

    def get_customer_by_id(self, customer_id):
        """Retrieve a customer by their ID."""
        if not self.customers:
            print("No customers available.")
            return None

        if customer_id not in self.customers:
            print(f"Customer with ID {customer_id} not found.")
            return None

        return self.customers[customer_id]

    def delete_customer(self, customer_id):
        """Delete a customer by their ID."""
        if customer_id in self.customers:
            del self.customers[customer_id]
        else:
            raise ValueError(f"No customer found with ID {customer_id}")
