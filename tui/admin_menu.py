# tui/admin_menu.py


def admin_login(warehouse, supplier_manager, finance_compiler):
    while True:
        print("\n--- Admin Alerts ---")
        low_stock_items = warehouse.inventory.low_stock_alerts()
        if low_stock_items:
            print("Low Stock Alerts:")
            for item in low_stock_items:
                quantity, threshold = warehouse.inventory.stock[item]
                print(f"- {item.name} (Qty: {quantity}, Threshold: {threshold})")

        print("\n--- Admin Menu ---")
        print("1. Manage Stock")
        print("2. Manage Finances")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            manage_stock(warehouse, supplier_manager)
        elif choice == "2":
            manage_finances(finance_compiler)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def manage_stock(warehouse, supplier_manager):
    while True:
        print("\n--- Manage Warehouse Stock ---")
        print("You're logged in as Admin at: ", warehouse.name)
        print("1. Order from Supplier")
        print("2. View Inventory")
        print("3. Edit Inventory Prices")
        print("4. Edit Inventory Stock Thresholds")
        print("5. Mark Order as Received")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            order_from_supplier(warehouse, supplier_manager)
        elif choice == "2":
            view_inventory(warehouse)
        elif choice == "3":
            edit_inventory_prices(warehouse)
        elif choice == "4":
            edit_inventory_thresholds(warehouse)
        elif choice == "5":
            mark_order_as_received(warehouse)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def order_from_supplier(warehouse, supplier_manager):
    print("\n--- Order from Supplier ---")

    try:
        suppliers = supplier_manager.get_all_suppliers()
    except ValueError as e:
        print(f"Error: {e}")
        return

    for supplier in suppliers:
        print(f"ID: {supplier.supplier_id} | Name: {supplier.name}")

    while True:
        supplier_id = input(
            "Enter the ID of the supplier to order from (or 'q' to cancel): "
        ).strip()
        if supplier_id.lower() == "q":
            return

        try:
            supplier = supplier_manager.get_supplier_by_id(supplier_id)
            break
        except ValueError as e:
            print(f"Error: {e}")

    print(f"\n--- Items Supplied by {supplier.name} ---")
    for idx, item in enumerate(supplier.items_supplied, start=1):
        print(f"{idx}. {item.name} - £{item.price:.2f}")

    while True:
        try:
            choice = int(input("Select item number to order: ")) - 1
            if choice < 0 or choice >= len(supplier.items_supplied):
                raise ValueError("Invalid item selection.")
            break
        except (ValueError, IndexError) as e:
            print(f"Error: {e}. Please select a valid item number.")

    try:
        quantity = int(input("Enter quantity to order: "))
        item = supplier.items_supplied[choice]

        order = warehouse.order_from_supplier(supplier, item, quantity)

        print(f"Ordered {quantity} of {item.name} from {supplier.name}.")
    except ValueError as e:
        print(f"Error: {e}. Order not placed.")


def view_inventory(warehouse):
    print("\n--- View Inventory ---")
    inventory = warehouse.view_inventory()

    if inventory:
        for item, (quantity, threshold) in inventory.items():
            print(f"{item} | Quantity: {quantity} | Threshold: {threshold}")


def edit_inventory_prices(warehouse):
    inventory = warehouse.inventory.get_full_item_info()
    if not inventory:
        print("Inventory is empty.")
        return

    print("\n--- Edit Inventory Prices ---")
    items = list(inventory.keys())
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item.name} (Current price: £{item.price:.2f})")

    try:
        choice = int(input("Select item to update price: "))
        if 1 <= choice <= len(items):
            item = items[choice - 1]
            new_price = float(input(f"Enter new price for {item.name}: "))
            warehouse.inventory.update_price(item.name, new_price)
            print(f"Price for {item.name} updated to £{new_price:.2f}.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def edit_inventory_thresholds(warehouse):
    try:
        inventory = warehouse.inventory.get_full_item_info()
    except ValueError as e:
        print(f"Error: {e}")
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

            try:
                warehouse.inventory.set_threshold(item.name, new_threshold)
                print(f"Threshold for {item.name} updated to {new_threshold}.")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def mark_order_as_received(warehouse):
    """Allow the admin to mark an order as received."""
    print("\n--- Mark Order as Received ---")

    pending_orders = warehouse.list_pending_orders()

    for idx, order in enumerate(pending_orders, start=1):
        print(
            f"{idx}. Order #{order.order_id}: {order.item.name} (Quantity: {order.quantity}) - Status: {order.status}"
        )

    try:
        choice = int(input("Select order number to mark as received: ")) - 1
        if 0 <= choice < len(pending_orders):
            order_to_mark = pending_orders[choice]
            warehouse.mark_order_as_received(order_to_mark.order_id)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")


def manage_finances(finance_compiler):
    """Manage finances related to orders and transactions."""
    while True:
        print("\n--- Manage Finances ---")
        print("1. View All Orders")
        print("2. Quick Financial Overview")
        print("3. Deep Dive into Financials")
        print("4. Export Financial Report")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_orders(finance_compiler)
        elif choice == "2":
            quick_financial_overview(finance_compiler)
        elif choice == "3":
            deep_dive_financials(finance_compiler)
        elif choice == "4":
            export_financial_report(finance_compiler)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def view_all_orders(finance_compiler):
    print("\n--- View All Orders ---")
    summaries = finance_compiler.summarise_orders()

    headers = [
        "Order ID",
        "Item",
        "Qty",
        "Price",
        "Total",
        "Buyer",
        "Seller",
        "Timestamp",
    ]
    print(
        f"{headers[0]:<10} {headers[1]:<15} {headers[2]:<5} {headers[3]:<7} {headers[4]:<8} {headers[5]:<15} {headers[6]:<15} {headers[7]}"
    )
    print("-" * 95)

    for s in summaries:
        print(
            f"{s['order_id']:<10} {s['item_name']:<15} {s['quantity']:<5} £{s['item_price']:<6.2f} £{s['total_price']:<7.2f} {s['buyer_name']:<15} {s['seller_name']:<15} {s['timestamp']}"
        )


def quick_financial_overview(finance_compiler):
    """Display a quick financial overview of revenue, costs, and profit."""
    print("\n--- Quick Financial Overview ---")
    total_revenue = finance_compiler.total_customer_revenue()
    total_costs = finance_compiler.total_supplier_costs()
    profit = finance_compiler.calculate_profit()

    print(f"Total Revenue from Customers: £{total_revenue:.2f}")
    print(f"Total Costs from Suppliers: £{total_costs:.2f}")
    print(f"Total Profit: £{profit:.2f}")


def deep_dive_financials(finance_compiler):
    """Provide a detailed analysis of orders and financials."""
    print("\n--- Deep Dive into Financials ---")
    customer_orders = finance_compiler.get_customer_orders()
    supplier_orders = finance_compiler.get_supplier_orders()

    print("\nCustomer Orders:")
    for order in customer_orders:
        print(
            f"Order ID: {order.order_id}, Item: {order.item.name}, Quantity: {order.quantity}, Total: £{order.total_price:.2f}"
        )

    print("\nSupplier Orders:")
    for order in supplier_orders:
        print(
            f"Order ID: {order.order_id}, Item: {order.item.name}, Quantity: {order.quantity}, Total: £{order.total_price:.2f}"
        )


def export_financial_report(finance_compiler):
    """Export a detailed financial report of all orders to CSV."""
    file_path = input(
        "Enter the file path to export the financial report (append .csv to the end): "
    )
    finance_compiler.export_orders_to_csv(finance_compiler.get_all_orders(), file_path)
    print(f"Financial report exported to {file_path}")
