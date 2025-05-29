from tui.admin_menu import admin_login
from tui.customer_menu import customer_login
from tui.supplier_menu import supplier_login
from app.supplier import SupplierManager
from app.customer import CustomerManager
from app.warehouse import Warehouse


def create_mock_customers(customer_manager):
    """Helper function to create mock customers"""
    customer_manager.create_customer("Bkar", "mock@mockemail.com", "1")
    customer_manager.create_customer("Aisha", "anothermock@mockemail.com", "2")


def create_mock_suppliers_and_items(supplier_manager):
    """Helper function to create mock suppliers and their items"""
    supplier_manager.create_supplier("Steve", "mocksupplier@mockemail.com", "1")
    supplier_manager.create_supplier("Alex", "mocksupplier@mockemail.com@", "2")

    supplier_manager.create_supplier_item("1", name="Dirt", description="Just dirt", price=10.0)
    supplier_manager.create_supplier_item("2", name="Cobblestone", description="Rough stone", price=20.0)
    supplier_manager.create_supplier_item("1", name="Oak Wood", description="Strong wood", price=15.0)
    supplier_manager.create_supplier_item("2", name="Birch Wood", description="Light wood", price=25.0)
    supplier_manager.create_supplier_item("1", name="Stone", description="Solid stone", price=30.0)
    supplier_manager.create_supplier_item("2", name="Iron Ore", description="Metallic ore", price=35.0)
    supplier_manager.create_supplier_item("1", name="Gold Ore", description="Shiny ore", price=40.0)
    supplier_manager.create_supplier_item("2", name="Spruce Wood", description="Dark wood", price=50.0)


def create_mock_orders(supplier_manager, warehouse):
    """Helper function to create some mock orders in the warehouse"""
    s1 = supplier_manager.get_supplier_by_id("1")
    s2 = supplier_manager.get_supplier_by_id("2")

    # Place some orders for different items from suppliers
    warehouse.order_from_supplier(s2, s2.items_supplied[0], 64)  # Cobblestone
    warehouse.order_from_supplier(s1, s1.items_supplied[0], 32)  # Dirt
    warehouse.order_from_supplier(s2, s2.items_supplied[0], 16)  # Cobblestone
    warehouse.order_from_supplier(s1, s1.items_supplied[0], 8)   # Dirt
    warehouse.order_from_supplier(s2, s2.items_supplied[0], 4)   # Cobblestone


def main_menu(supplier_manager, customer_manager, warehouse):
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Supplier Login")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            admin_login(warehouse, supplier_manager)
        elif choice == '2':
            customer_login(customer_manager, warehouse)
        elif choice == '3':
            supplier_login(supplier_manager)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Initialize managers and warehouse
    supplier_manager = SupplierManager()
    customer_manager = CustomerManager()
    warehouse = Warehouse(name="Main Warehouse")

    # Create mock data for customers, suppliers, and items
    create_mock_customers(customer_manager)
    create_mock_suppliers_and_items(supplier_manager)
    create_mock_orders(supplier_manager, warehouse)

    # Start the main menu
    main_menu(supplier_manager, customer_manager, warehouse)
