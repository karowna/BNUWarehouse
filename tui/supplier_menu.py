def supplier_login(supplier_manager):
    while True:
        print("\n--- Supplier Login ---")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            supplier_sign_up(supplier_manager)
        elif choice == '2':
            supplier_sign_in(supplier_manager)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

def supplier_sign_up(supplier_manager):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    supplier_id = input("Enter a unique supplier ID: ")
    try:
        supplier_manager.create_supplier(name, email, supplier_id)
        print(f"Supplier {name} created successfully! Your supplier ID is {supplier_id}.")
    except ValueError as e:
        print(e)

def supplier_sign_in(supplier_manager):
    supplier_id = input("Enter your supplier ID: ")
    supplier = supplier_manager.get_supplier_by_id(supplier_id)
    if supplier:
        print(f"\nWelcome back, {supplier.name}!")
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
    name = input("Enter item name: ")
    description = input("Enter item description: ")
    try:
        price = float(input("Enter item price: "))
        item = supplier_manager.create_supplier_item(
            supplier_id=supplier.supplier_id,
            name=name,
            description=description,
            price=price
        )
        print(f"Item '{item.name}' created successfully.")
    except ValueError as e:
        print(f"Error: {e}")

def view_supplier_items(supplier):
    items = supplier_manager.get_supplier_items(supplier.supplier_id)
    if items:
        print("\n--- Items Supplied ---")
        for item in items:
            print(f"{item.name}: {item.description} - £{item.price:.2f}")
    else:
        print("No items found.")
