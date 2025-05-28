from app.customer import Customer, CustomerManager

customer_manager = CustomerManager()

# Create mock customers for demonstration
customer_manager.create_customer("Bkar", "mock@mockemail.com", "1")
customer_manager.create_customer("Aisha","anothermock@mockemail.com","2")

def customer_login():
    while True:
        print("\n--- Customer Login ---")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            sign_up()
        elif choice == '2':
            sign_in()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def sign_up():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    customer_id = input("Enter a unique customer ID: ")
    try:
        customer_manager.create_customer(name, email, customer_id)
        print(f"Customer {name} created successfully! Your customer ID is {customer_id}.")
    except ValueError as e:
        print(e)

def sign_in():
    customer_id = input("Enter your customer ID: ")
    customer = customer_manager.get_customer_by_id(customer_id)
    if customer:
        print(f"Welcome back, {customer.name}!")
        customer_menu(customer)
    else:
        print("Customer not found. Please sign up first.")

def customer_menu(customer):
    while True:
        print("\n--- Customer Menu ---")
        print("1. Browse Warehouse Items")
        print("2. Make an Order")
        print("3. View Order History")
        print("4. Update Profile")
        print("5. View Profile")
        print("0. Log Out")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_profile(customer)
        elif choice == '2':
            update_profile(customer)
        elif choice == '3':
            view_order_history(customer)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def view_profile(customer):
    print(f"\n--- Profile of {customer.name} ---")
    print(f"Customer ID: {customer.customer_id}")
    print(f"Email: {customer.email}")

def update_profile(customer):
    print("\n--- Update Profile ---")
    name = input("Enter new name (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")
    
    if name:
        customer.name = name
    if email:
        customer.email = email
    
    print("Profile updated successfully!")

def view_order_history(customer):
    print("\n--- Order History ---")
    if customer.order_history:
        for order in customer.order_history:
            print(f"Order ID: {order['order_id']}, Items: {order['items']}, Total: {order['total']}")
    else:
        print("No orders found.")

