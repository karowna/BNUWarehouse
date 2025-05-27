class Customer(Person):

    def __init__(self, name, email, person_id):
        super().__init__(person_id, name, email) # Using the Person constructor via Super
        self.order_history = [] 

    @property # Property to alias the person_id as customer_id to make things more readable
    def customer_id(self):
        return self.person_id

    def view_order_history(self):
        return self.order_history

class CustomerManager: # Manages customer objects, customer should not manage itself
    pass