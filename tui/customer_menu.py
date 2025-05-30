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
    try:
        customer = customer_manager.create_customer(name, email)
        print(f"Customer {name} created successfully! Your customer ID is {customer.customer_id}. Remember it!")
    except ValueError as e:
        print(e)


def sign_in(customer_manager, warehouse):
    customer_id = input("Enter your customer ID: ")
    customer = customer_manager.get_customer_by_id(customer_id)

    if customer:
        print(f"\nWelcome back, {customer.name}!")
        customer_menu(customer, warehouse)


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
            place_order(customer, warehouse)
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
    filtered_items = warehouse.get_available_items()

    for item, quantity in filtered_items.items():
        print(f"Name: {item.name}, Price: £{item.price:.2f}, Quantity Available: {quantity}")


def place_order(customer, warehouse):
    print("\n--- Place an Order ---")
    stock_info = warehouse.get_available_items()

    items = list(stock_info.keys())

    for idx, item in enumerate(items, start=1):
        available_qty = stock_info[item]
        print(f"{idx}. {item.name} - £{item.price:.2f} (Available: {available_qty})")

    try:
        choice = int(input("Select item number to order: ")) - 1
        quantity = int(input("Enter quantity to order: "))

        item = items[choice]
        order = warehouse.place_order(customer, item, quantity)

        print(f"Order placed: {quantity} x {item.name} (£{order.total_price:.2f})")

    except (ValueError, IndexError) as e:
        print(f"Invalid input or selection: {e}")
    except Exception as e:
        print(f"Error placing order: {e}")


def view_profile(customer):
    """Display the customer's profile information.""" # Can just access the customer object directly
    print(f"\n--- Profile of {customer.name} ---")
    print(f"Customer ID: {customer.customer_id}")
    print(f"Email: {customer.email}")

def update_profile(customer):
    """Update the customer's profile information."""
    print("\n--- Update Profile ---")
    name = input("Enter new name (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")
    
    customer.update_profile(name=name, email=email)
    
    print("Profile updated successfully!")

def view_order_history(customer):
    """Display the customer's order history."""
    print("\n--- Order History ---")
    
    if not customer.order_history:
        print("No orders found.")
        return

    headers = ["Order ID", "Item", "Quantity", "Price", "Total", "Seller", "Status", "Timestamp"]
    print(f"{headers[0]:<10} {headers[1]:<15} {headers[2]:<8} {headers[3]:<8} {headers[4]:<8} "
          f"{headers[5]:<15} {headers[6]:<10} {headers[7]}")
    print("-" * 105)

    for order in customer.order_history:
        print(f"{order.order_id:<10} {order.item.name:<15} {order.quantity:<8} "
              f"£{order.item.price:<7.2f} £{order.total_price:<7.2f} "
              f"{getattr(order.seller, 'name', 'Warehouse'):<15} {order.status:<10} "
              f"{order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
