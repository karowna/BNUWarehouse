# tui/main.py

import sys

from tui.admin_menu import admin_login
from tui.customer_menu import customer_login
from tui.supplier_menu import supplier_login
from app.supplier import SupplierManager
from app.customer import CustomerManager
from app.warehouse import Warehouse
from app.finance import FinanceCompiler

# Import the mock data loader, but only call it if needed
USE_MOCK_DATA = "--mock" in sys.argv

if USE_MOCK_DATA:
    from tests.mock_data import import_mock_data

    customer_manager, supplier_manager, warehouse = import_mock_data()
else:
    customer_manager = CustomerManager()
    supplier_manager = SupplierManager()
    warehouse = Warehouse(name="Main Warehouse")

finance_compiler = FinanceCompiler(orders=warehouse.orders)


def main_menu(supplier_manager, customer_manager, warehouse):
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Supplier Login")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            admin_login(warehouse, supplier_manager, finance_compiler)
        elif choice == "2":
            customer_login(customer_manager, warehouse)
        elif choice == "3":
            supplier_login(supplier_manager)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu(supplier_manager, customer_manager, warehouse)
