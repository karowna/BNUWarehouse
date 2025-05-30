import csv
from typing import List
from app.order import Order

class FinanceCompiler:
    """A class to compile financial data from orders"""

    def __init__(self, orders: List[Order]):
        self.orders = orders

    def total_customer_revenue(self) -> float:
        """Calculate total revenue from customer orders with status 'delivered'"""
        customer_orders = [
            order for order in self.orders
            if order.seller.__class__.__name__ == 'Warehouse' and order.status == 'delivered'
        ]

        if not customer_orders:
            print("Warning: No delivered customer orders found.")
            return 0.0

        return sum(order.total_price for order in customer_orders)

    def total_supplier_costs(self) -> float:
        """Calculate total costs from supplier orders with status 'received'"""
        supplier_orders = [
            order for order in self.orders
            if order.seller.__class__.__name__ == 'Supplier' and order.status == 'received'
        ]

        if not supplier_orders:
            print("Warning: No received supplier orders found.")
            return 0.0

        return sum(order.total_price for order in supplier_orders)


    def calculate_profit(self) -> float:
        """Calculate profit (customer revenue - supplier costs)"""
        customer_revenue = self.total_customer_revenue()
        supplier_costs = self.total_supplier_costs()

        # Check if there's no revenue or costs
        if customer_revenue == 0:
            print("No customer revenue found.")
        if supplier_costs == 0:
            print("No supplier costs found.")

        return customer_revenue - supplier_costs


    def get_customer_orders(self) -> List[Order]:
        """Get all customer orders with status 'delivered'"""
        customer_orders = [order for order in self.orders
                        if order.seller.__class__.__name__ == 'Warehouse' and order.status == 'delivered']

        # Check if there are no customer orders delivered
        if not customer_orders:
            print("No customer orders with 'delivered' status found.")

        return customer_orders


    def get_supplier_orders(self) -> List[Order]:
        """Get all supplier orders with status 'received'"""
        supplier_orders = [order for order in self.orders
                        if order.seller.__class__.__name__ == 'Supplier' and order.status == 'received']

        if not supplier_orders:
            print("No supplier orders with 'received' status found.")

        return supplier_orders


    def get_all_orders(self) -> List[Order]:
        """Get all orders (regardless of status)"""
        all_orders = self.orders

        if not all_orders:
            print("No orders found.")

        return all_orders


    def display_orders(self, orders: List[Order]):
        """Display orders in a formatted table"""
        print(f"{'Order ID':<10} {'Item':<15} {'Qty':<5} {'Total':<10} {'Buyer':<15} {'Seller':<15} {'Status':<10} {'Date'}")
        print("-" * 105)
        for order in orders:
            print(f"{order.order_id:<10} {order.item.name:<15} {order.quantity:<5} £{order.total_price:<8.2f} "
                  f"{getattr(order.buyer, 'name', 'N/A'):<15} {getattr(order.seller, 'name', 'N/A'):<15} "
                  f"{order.status:<10} {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    def export_orders_to_csv(self, orders: List[Order], file_path: str):
        """Export orders to a CSV file"""
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Order ID", "Item", "Quantity", "Total Price", "Buyer", "Seller", "Status", "Date"])
            for order in orders:
                writer.writerow([
                    order.order_id,
                    order.item.name,
                    order.quantity,
                    f"£{order.total_price:.2f}",
                    getattr(order.buyer, 'name', 'N/A'),
                    getattr(order.seller, 'name', 'N/A'),
                    order.status,
                    order.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                ])

    def _summarise_order(self, order: Order) -> dict:
        """Helper function to summarize a single order"""
        return {
            "order_id": order.order_id,
            "item_name": order.item.name,
            "item_description": order.item.description,
            "item_price": order.item.price,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "buyer_name": getattr(order.buyer, 'name', 'N/A'),
            "seller_name": getattr(order.seller, 'name', 'N/A'),
            "status": order.status,
            "timestamp": order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

 def summarise_orders(self) -> List[dict]:
        """Summarizes all orders in the system and prints a message if there are no orders."""
        if not self.orders:
            print("No orders found.")
            return []

        return [self._summarise_order(order) for order in self.orders]
