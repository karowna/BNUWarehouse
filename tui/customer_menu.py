def customer_login(customer_manager, warehouse):
    while True:
        print("\n--- Customer Login ---")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            sign_up(customer_manager)
        elif choice == '2':
            sign_in(customer_manager, warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def sign_up(customer_manager):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    customer_id = input("Enter a unique customer ID: ")
    try:
        customer_manager.create_customer(name, email, customer_id)
        print(f"Customer {name} created successfully! Your customer ID is {customer_id}.")
    except ValueError as e:
        print(e)

def sign_in(customer_manager, warehouse):
    customer_id = input("Enter your customer ID: ")
    customer = customer_manager.get_customer_by_id(customer_id)
    if customer:
        print(f"\nWelcome back, {customer.name}!")
        customer_menu(customer, warehouse)
    else:
        print("Customer not found. Please sign up first.")

def customer_menu(customer, warehouse):
    """Main menu for the customer to navigate through the available actions."""
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
            browse_warehouse_items(warehouse)
        elif choice == '2':
            make_order(customer, warehouse)
        elif choice == '3':
            view_order_history(customer)
        elif choice == '4':
            update_profile(customer)
        elif choice == '5':
            view_profile(customer)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def browse_warehouse_items(warehouse):
    """Allow the customer to browse available items in the warehouse."""
    print("\n--- Browse Warehouse Items ---")
    items = warehouse.get_available_stock()  # Assuming this returns a list of items
    if not items:
        print("No items available in the warehouse.")
        return

    for item in items:
        print(f"Item ID: {item.item_id}, Name: {item.name}, Price: {item.price}, Quantity: {item.stock}")

def make_order(customer, warehouse):
    """Allow the customer to make an order."""
    print("\n--- Make an Order ---")
    item_id = input("Enter the item ID to order: ")
    quantity = int(input("Enter the quantity: "))
    
    item = warehouse.get_item_by_id(item_id)
    if not item:
        print("Item not found in the warehouse.")
        return

    if item.stock < quantity:
        print(f"Insufficient stock. Only {item.stock} items are available.")
        return

    # Create the order
    order = warehouse.create_order(customer, item, quantity)
    print(f"Order placed successfully! Order ID: {order['order_id']}, Total: {order['total']}")

    # Add the order to the customer's order history
    customer.order_history.append(order)

def view_profile(customer):
    """Display the customer's profile information."""
    print(f"\n--- Profile of {customer.name} ---")
    print(f"Customer ID: {customer.customer_id}")
    print(f"Email: {customer.email}")

def update_profile(customer):
    """Update the customer's profile information."""
    print("\n--- Update Profile ---")
    name = input("Enter new name (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")
    
    # Use the Customer's update_profile method to manage updates
    customer.update_profile(name=name if name else None, email=email if email else None)
    
    print("Profile updated successfully!")

def view_order_history(customer):
    """Display the customer's order history."""
    print("\n--- Order History ---")
    if customer.order_history:
        for order in customer.order_history:
            print(f"Order ID: {order['order_id']}, Items: {order['items']}, Total: {order['total']}")
    else:
        print("No orders found.")
