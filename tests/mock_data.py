from app.supplier import SupplierManager
from app.customer import CustomerManager
from app.warehouse import Warehouse


def create_mock_customers(customer_manager):
    """Helper function to create mock customers."""
    customer_manager.create_customer("Bkar", "mock@mockemail.com")
    customer_manager.create_customer("Aisha", "anothermock@mockemail.com")


def create_mock_suppliers_and_items(supplier_manager):
    """Helper function to create mock suppliers and their items."""
    supplier1 = supplier_manager.create_supplier("Steve", "mocksupplier@mockemail.com")
    supplier2 = supplier_manager.create_supplier("Alex", "mocksupplier@mockemail.com")

    supplier_manager.create_supplier_item(
        supplier1.supplier_id, name="Dirt", description="Just dirt", price=10.0
    )
    supplier_manager.create_supplier_item(
        supplier2.supplier_id, name="Cobblestone", description="Rough stone", price=20.0
    )
    supplier_manager.create_supplier_item(
        supplier1.supplier_id, name="Oak Wood", description="Strong wood", price=15.0
    )
    supplier_manager.create_supplier_item(
        supplier2.supplier_id, name="Birch Wood", description="Light wood", price=25.0
    )
    supplier_manager.create_supplier_item(
        supplier1.supplier_id, name="Stone", description="Solid stone", price=30.0
    )
    supplier_manager.create_supplier_item(
        supplier2.supplier_id, name="Iron Ore", description="Metallic ore", price=35.0
    )
    supplier_manager.create_supplier_item(
        supplier1.supplier_id, name="Gold Ore", description="Shiny ore", price=40.0
    )
    supplier_manager.create_supplier_item(
        supplier2.supplier_id, name="Spruce Wood", description="Dark wood", price=50.0
    )


def create_mock_orders_to_supplier(supplier_manager, warehouse):
    """Helper function to create stock and orders within the warehouse."""
    supplier1 = supplier_manager.get_supplier_by_id("su_1")
    supplier2 = supplier_manager.get_supplier_by_id("su_2")

    # Create a list to keep track of placed orders
    orders_to_receive = []

    # Place some orders for different items from suppliers
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier2, supplier2.items_supplied[0], 128)
    )  # Cobblestone
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier1, supplier1.items_supplied[0], 64)
    )  # Dirt
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier2, supplier2.items_supplied[0], 32)
    )  # Cobblestone
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier1, supplier1.items_supplied[0], 16)
    )  # Dirt
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier2, supplier2.items_supplied[0], 8)
    )  # Cobblestone
    orders_to_receive.append(
        warehouse.order_from_supplier(supplier1, supplier1.items_supplied[3], 100)
    )  # Gold Ore

    # Mark each order as received
    for order in orders_to_receive:
        order.status = "received"
        warehouse.inventory.add_stock(order.item, order.quantity)

    warehouse.order_from_supplier(
        supplier1, supplier1.items_supplied[1], 128
    )  # Oak Wood, add some in to see them pending
    warehouse.order_from_supplier(
        supplier2, supplier2.items_supplied[1], 64
    )  # Birch Wood, add some in to see them pending

    # Update price of gold ore in the warehouse inventory, turns over a profit
    warehouse.inventory.update_price("Gold Ore", 500)
    warehouse.inventory.set_threshold


def create_mock_orders_to_warehouse(customer_manager, warehouse):
    """Create mock orders from customers to the warehouse."""
    customer1 = customer_manager.get_customer_by_id("cu_1")
    customer2 = customer_manager.get_customer_by_id("cu_2")

    # Find the Gold Ore item in warehouse inventory keys
    gold_ore_item = None
    for item in warehouse.inventory.stock.keys():
        if item.name == "Gold Ore":
            gold_ore_item = item
            break

    order1 = warehouse.place_order(customer1, gold_ore_item, 5)
    order2 = warehouse.place_order(customer2, gold_ore_item, 10)
    order3 = warehouse.place_order(customer1, gold_ore_item, 80)

    warehouse.inventory.set_threshold(
        "Gold Ore", 10
    )  # Threshold should show up on the alerts menu


def import_mock_data():
    """Import mock data for testing."""
    customer_manager = CustomerManager()
    supplier_manager = SupplierManager()
    warehouse = Warehouse("Main Warehouse")

    # Create mock customers
    create_mock_customers(customer_manager)

    # Create mock suppliers and items
    create_mock_suppliers_and_items(supplier_manager)

    # Create mock orders to suppliers
    create_mock_orders_to_supplier(supplier_manager, warehouse)

    # Create mock orders to warehouse
    create_mock_orders_to_warehouse(customer_manager, warehouse)

    return customer_manager, supplier_manager, warehouse
