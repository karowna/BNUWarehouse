from customer import Customer, CustomerManager


def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Login")
        print("2. Customer Login")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            admin_login()
        elif choice == '2':
            customer_login()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

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
    else:
        print("Customer not found. Please sign up first.")

def admin_login():
    print("\n--- Admin Menu ---")
    print("1. Manage Suppliers")
    print("2. Manage Stock")
    print("3. Manage Finances")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")

        if choice == '1':
            manage_suppliers()
        elif choice == '2':
            manage_stock()
        elif choice == '3':
            manage_finances()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_suppliers():
    print("\n--- Manage Suppliers ---")
    # Placeholder for supplier management logic
    print("Supplier management functionality is not yet implemented.")

def manage_stock():
    print("\n--- Manage Stock ---")
    # Placeholder for stock management logic
    print("Stock management functionality is not yet implemented.")

def manage_finances():
    print("\n--- Manage Finances ---")
    # Placeholder for finance management logic
    print("Finance management functionality is not yet implemented.")


if __name__ == "__main__": # Starting point of the application (TUI)
    customer_manager = CustomerManager() # Initialize a customer manager object
    main_menu()

