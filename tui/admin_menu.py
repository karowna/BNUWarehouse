def admin_login(warehouse, supplier_manager):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Manage Stock")
        print("2. Manage Finances")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_stock(warehouse)
        elif choice == '2':
            manage_finances()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_stock(warehouse):
    while True:
        print("\n--- Manage Warehouse Stock ---")
        print("1. Order from Supplier")
        print("2. View Inventory")
        print("3. Edit Inventory Prices")
        print("4. Edit Inventory Stock Thresholds")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            order_from_supplier(warehouse)
        elif choice == '2':
            view_inventory(warehouse)
        elif choice == '3':
            edit_inventory_prices(warehouse)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def order_from_supplier(supplier_manager):
    suppliers = supplier_manager.get_all_suppliers()
    if not suppliers:
        print("No suppliers available.")
        return None

    print("\n--- Available Suppliers ---")
    for supplier in suppliers:
        print(f"ID: {supplier.supplier_id} | Name: {supplier.name}")

    supplier_id = input("Enter the ID of the supplier you want to view: ")
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
        print(f"{idx}. ID: {id(item)} | Name: {item.name} | Price: ${item.price:.2f}")

    return supplier


def view_inventory(warehouse):
    print("\n--- View Inventory ---")
    inventory = warehouse.view_inventory()
    if not inventory:
        print("No items in inventory.")
    else:
        for item, details in inventory.items():
            print(f"Item: {item}, Quantity: {details['quantity']}, Price: {details['price']}")

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


def manage_finances():
    print("\n--- Manage Finances ---")
    # Placeholder for finance management logic
    print("Finance management functionality is not yet implemented.")
