def admin_login(warehouse, supplier_manager):
    while True:
        print("\n--- Admin Alerts ---")
        low_stock_items = warehouse.inventory.low_stock_alerts()
        if low_stock_items:
            print("Low Stock Alerts:")
            for item in low_stock_items:
                quantity, threshold = warehouse.inventory.stock[item]
                print(f"- {item.name} (Qty: {quantity}, Threshold: {threshold})")
        else:
            print("Nothing to report.")

        print("\n--- Admin Menu ---")
        print("1. Manage Stock")
        print("2. Manage Finances")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_stock(warehouse, supplier_manager)
        elif choice == '2':
            manage_finances(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def manage_stock(warehouse, supplier_manager):
    while True:
        print("\n--- Manage Warehouse Stock ---")
        print("1. Order from Supplier")
        print("2. View Inventory")
        print("3. Edit Inventory Prices")
        print("4. Edit Inventory Stock Thresholds")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            order_from_supplier(warehouse, supplier_manager)
        elif choice == '2':
            view_inventory(warehouse)
        elif choice == '3':
            edit_inventory_prices(warehouse)
        elif choice == '4':
            edit_inventory_thresholds(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def order_from_supplier(warehouse, supplier_manager):
    suppliers = supplier_manager.get_all_suppliers()
    if not suppliers:
        print("No suppliers available.")
        return None

    print("\n--- Available Suppliers ---")
    for supplier in suppliers:
        print(f"ID: {supplier.supplier_id} | Name: {supplier.name}")

    supplier_id = input("Enter the ID of the supplier you want to order from: ")
    supplier = supplier_manager.get_supplier_by_id(supplier_id)

    if not supplier:
        print("Supplier not found.")
        return None

    items = supplier.items_supplied
    if not items:
        print(f"{supplier.name} has no items.")
        return supplier

    print(f"\n--- Items Supplied by {supplier.name} ---")
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. Name: {item.name} | Price: £{item.price:.2f}")

    try:
        item_choice = int(input("Enter the number of the item you want to order: ")) - 1
        if item_choice < 0 or item_choice >= len(items):
            print("Invalid item selection.")
            return None

        quantity = int(input("Enter the quantity to order: "))
        if quantity <= 0:
            print("Quantity must be positive.")
            return None

        item = items[item_choice]
        warehouse.order_from_supplier(supplier, item, quantity)
        print(f"Ordered {quantity} of {item.name} from {supplier.name}.")

    except ValueError:
        print("Invalid input. Please enter numeric values.")

    return supplier


def view_inventory(warehouse):
    print("\n--- View Inventory ---")
    inventory = warehouse.view_inventory()
    if not inventory:
        print("No items in inventory.")
    else:
        for item, (quantity, threshold) in warehouse.inventory.get_full_stock_info().items():
            print(f"{item} | Quantity: {quantity} | Threshold: {threshold}")

def edit_inventory_prices(warehouse):
    print("\n--- Edit Inventory Prices ---")
    item = input("Enter Item Name: ")
    new_price = float(input("Enter New Price: "))
    
    try:
        warehouse.inventory.update_price(item, new_price)
        print(f"Price for {item} updated to {new_price}.")
    except ValueError as e:
        print(e)

def edit_inventory_thresholds(warehouse):
    inventory = warehouse.inventory.get_full_stock_info()
    if not inventory:
        print("Inventory is empty.")
        return

    print("\n--- Edit Inventory Stock Thresholds ---")
    items = list(inventory.keys())
    for idx, item in enumerate(items, start=1):
        _, current_threshold = inventory[item]
        print(f"{idx}. {item.name} (Current threshold: {current_threshold})")

    try:
        choice = int(input("Select item to update threshold: "))
        if 1 <= choice <= len(items):
            item = items[choice - 1]
            new_threshold = int(input(f"Enter new threshold for {item.name}: "))
            warehouse.inventory.set_threshold(item, new_threshold)
            print(f"Threshold for {item.name} updated to {new_threshold}.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

def manage_finances(warehouse):
    while True:
        print("\n--- Manage Finances ---")
        print("1. View All Orders")
        print("2. Quick Financial Overview")
        print("3. Deep Dive into Financials")
        print("4. Export Financial Report")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_all_orders(warehouse)
        elif choice == '2':
            quick_financial_overview(warehouse)
        elif choice == '3':
            deep_dive_financials(warehouse)
        elif choice == '4':
            export_financial_report(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def view_all_orders(warehouse):
    print("\n--- View All Orders ---")
    summaries = warehouse.summarise_orders()
    if not summaries:
        print("No orders found.")
        return

    headers = ["Order ID", "Item", "Qty", "Price", "Total", "Buyer", "Seller", "Timestamp"]
    print(f"{headers[0]:<10} {headers[1]:<15} {headers[2]:<5} {headers[3]:<7} {headers[4]:<8} {headers[5]:<15} {headers[6]:<15} {headers[7]}")
    print("-" * 95)

    for s in summaries:
        print(f"{s['order_id']:<10} {s['item_name']:<15} {s['quantity']:<5} £{s['item_price']:<6.2f} £{s['total_price']:<7.2f} {s['buyer_name']:<15} {s['seller_name']:<15} {s['timestamp']}")


def quick_financial_overview(warehouse):
    pass

def deep_dive_financials(warehouse):
    pass

def export_financial_report(warehouse):
    pass

