def admin_login():
    while True:
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
    print("1. View Suppliers")
    print("2. Add Supplier")
    print("3. Update Supplier")
    print("4. Delete Supplier")
    print("5. View Supplier Items")
    print("6. Add Item to Supplier")
    print("7. Remove Item from Supplier")
    print("0. Back to Admin Menu")

    choice = input("Enter your choice: ")

def manage_stock():
    print("\n--- Manage Stock ---")
    # Placeholder for stock management logic
    print("Stock management functionality is not yet implemented.")

def manage_finances():
    print("\n--- Manage Finances ---")
    # Placeholder for finance management logic
    print("Finance management functionality is not yet implemented.")
