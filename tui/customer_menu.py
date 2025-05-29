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
        
def browse_warehouse_items(warehouse):
    print("\n--- Browse Warehouse Items ---")
    filtered_items = warehouse.get_items_above_threshold()

    if not filtered_items:
        print("No items available at the moment.")
        return

    for item, (quantity, _) in filtered_items.items():
        print(f"Name: {item.name}, Price: £{item.price:.2f}, Quantity: {quantity}")

def make_order(customer, warehouse):
    print("\n--- Make an Order ---")
    stock = warehouse.get_items_above_threshold()

    if not stock:
        print("No items available to order.")
        return

    # Display available items
    items = list(stock.keys())
    for idx, item in enumerate(items, start=1):
        qty = stock[item][0]
        print(f"{idx}. {item.name} - £{item.price:.2f} (Available: {qty})")

    try:
        choice = int(input("Select item number to order: ")) - 1
        if not (0 <= choice < len(items)):
            print("Invalid selection.")
            return

        item = items[choice]
        quantity = int(input(f"Enter quantity to order (max {stock[item][0]}): "))
        if quantity <= 0 or quantity > stock[item][0]:
            print("Invalid quantity.")
            return

        # Create and process the order
        from app.order import Order  # only if needed
        order = Order(item=item, quantity=quantity, buyer=customer, seller=warehouse)
        warehouse.process_order(order)

        # Add to customer's history
        if not hasattr(customer, "order_history"):
            customer.order_history = []
        customer.order_history.append(order)


        print(f"Order placed: {quantity} x {item.name} (£{order.total_price:.2f})")

    except ValueError:
        print("Invalid input. Please enter numbers.")



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
    
    if not customer.order_history:
        print("No orders found.")
        return

    # Print header
    headers = ["Order ID", "Item", "Quantity", "Price", "Total", "Seller", "Timestamp"]
    print(f"{headers[0]:<10} {headers[1]:<15} {headers[2]:<8} {headers[3]:<8} {headers[4]:<8} {headers[5]:<15} {headers[6]}")
    print("-" * 90)

    # Print each order
    for order in customer.order_history:
        print(f"{order.order_id:<10} {order.item.name:<15} {order.quantity:<8} "
              f"£{order.item.price:<7.2f} £{order.total_price:<7.2f} "
              f"{getattr(order.seller, 'name', 'Warehouse'):<15} "
              f"{order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
