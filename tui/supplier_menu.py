from app.supplier import Supplier, SupplierManager

supplier_manager = SupplierManager()

def supplier_login():
    while True:
        print("\n--- Supplier Login ---")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            supplier_sign_up()
        elif choice == '2':
            supplier_sign_in()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def supplier_sign_up():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    supplier_id = input("Enter a unique supplier ID: ")
    try:
        supplier_manager.create_supplier(name, email, supplier_id)
        print(f"Supplier {name} created successfully! Your supplier ID is {supplier_id}.")
    except ValueError as e:
        print(e)

def supplier_sign_in():
    supplier_id = input("Enter your supplier ID: ")
    supplier = supplier_manager.get_supplier_by_id(supplier_id)
    if supplier:
        print(f"Welcome back, {supplier.name}!")
        supplier_menu(supplier)
    else:
        print("Supplier not found. Please sign up first.")

def supplier_menu(supplier):
    while True:
        print("\n--- Supplier Menu ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Create Item")
        print("4. View Items")
        print("5. Remove Item")
        print("0. Log Out")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_supplier_profile(supplier)
        elif choice == '2':
            update_supplier_profile(supplier)
        elif choice == '3':
            create_item_for_supplier(supplier)
        elif choice == '4':
            view_supplier_items(supplier)
        elif choice == '5':
            remove_item_from_supplier(supplier)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def view_supplier_profile(supplier):
    print(f"Name: {supplier.name}")
    print(f"Email: {supplier.email}")
    print(f"Supplier ID: {supplier.supplier_id}")

def update_supplier_profile(supplier):
    name = input("Enter new name (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")
    if name:
        supplier.name = name
    if email:
        supplier.email = email
    print("Profile updated successfully.")

def create_item_for_supplier(supplier):
    from item import Item
    name = input("Enter item name: ")
    description = input("Enter item description: ")
    price = float(input("Enter item price: "))
    item = Item(name, description, price, supplier)
    supplier_manager.add_item_to_supplier(supplier.supplier_id, item)
    print(f"Item {name} created successfully.")

def view_supplier_items(supplier):
    items = supplier_manager.get_supplier_items(supplier.supplier_id)
    if items:
        print("\n--- Items Supplied ---")
        for item in items:
            print(f"{item.name}: {item.description} - ${item.price:.2f}")
    else:
        print("No items found.")

def remove_item_from_supplier(supplier):
    items = supplier_manager.get_supplier_items(supplier.supplier_id)
    if items:
        print("\n--- Items Supplied ---")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item.name}: {item.description} - ${item.price:.2f}")
        choice = int(input("Enter the number of the item to remove: "))
        if 1 <= choice <= len(items):
            item = items[choice - 1]
            supplier_manager.remove_item_from_supplier(supplier.supplier_id, item)
            print(f"Item {item.name} removed successfully.")
        else:
            print("Invalid choice.")
    else:
        print("No items found.")
