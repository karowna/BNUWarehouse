# tui/supplier_menu.py


def supplier_login(supplier_manager):
    while True:
        print("\n--- Supplier Login ---")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            supplier_sign_up(supplier_manager)
        elif choice == "2":
            supplier_sign_in(supplier_manager)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def supplier_sign_up(supplier_manager):
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    try:
        supplier = supplier_manager.create_supplier(name, email)
        print(
            f"Supplier {name} created successfully! Your supplier ID is {supplier.supplier_id} Remember it!."
        )
    except ValueError as e:
        print(e)


def supplier_sign_in(supplier_manager):
    supplier_id = input("Enter your supplier ID: ")
    supplier = supplier_manager.get_supplier_by_id(supplier_id)

    if supplier:
        print(f"\nWelcome back, {supplier.name}!")
        supplier_menu(supplier_manager, supplier)


def supplier_menu(supplier_manager, supplier):
    while True:
        print("\n--- Supplier Menu ---")
        print(f"You're logged in as: {supplier.name} (ID: {supplier.supplier_id})")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Create Item")
        print("4. View Items")
        print("5. Remove Item")
        print("0. Log Out")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_supplier_profile(supplier)
        elif choice == "2":
            update_supplier_profile(supplier)
        elif choice == "3":
            create_item_for_supplier(supplier_manager, supplier)
        elif choice == "4":
            view_supplier_items(supplier_manager, supplier)
        elif choice == "5":
            remove_item_from_supplier(supplier_manager, supplier)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def view_supplier_profile(supplier):
    print(f"\n--- Profile of {supplier.name} ---")
    print(f"Email: {supplier.email}")
    print(f"Supplier ID: {supplier.supplier_id}")


def update_supplier_profile(supplier):
    name = input("Enter new name (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")

    supplier.update_profile(name=name if name else None, email=email if email else None)

    print("Profile updated successfully.")


def create_item_for_supplier(supplier_manager, supplier):
    name = input("Enter item name: ")
    description = input("Enter item description: ")
    try:
        price = float(input("Enter item price: "))
        item = supplier_manager.create_supplier_item(
            supplier.supplier_id, name, description, price
        )
        print(f"Item '{item.name}' created successfully.")
    except ValueError as e:
        print(f"Error: {e}")


def view_supplier_items(supplier_manager, supplier):
    try:
        items = supplier_manager.get_supplier_items(supplier.supplier_id)
        print("\n--- Items Supplied ---")
        for item in items:
            print(f"{item.name}: {item.description} - £{item.price:.2f}")
    except ValueError as e:
        print(str(e))


def remove_item_from_supplier(supplier_manager, supplier):
    try:
        items = supplier_manager.get_supplier_items(supplier.supplier_id)

        print("\n--- Items Supplied ---")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item.name}: {item.description} - £{item.price:.2f}")

        item_choice = (
            int(input("Enter the number of the item you want to remove: ")) - 1
        )
        if item_choice < 0 or item_choice >= len(items):
            print("Invalid item selection.")
            return

        item = items[item_choice]
        supplier_manager.remove_item_from_supplier(supplier.supplier_id, item)
        print(f"Item '{item.name}' removed successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
