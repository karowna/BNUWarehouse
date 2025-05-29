import csv
from typing import List
from app.order import Order

class FinanceCompiler:
    """A class to compile financial data from orders"""

    def __init__(self, orders: List[Order]):
        self.orders = orders

    def total_customer_revenue(self) -> float:
        """Calculate total revenue from customer orders"""
        return sum(order.total_price for order in self.orders if order.seller.__class__.__name__ == 'Warehouse')

    def total_supplier_costs(self) -> float:
        """Calculate total costs from supplier orders"""
        return sum(order.total_price for order in self.orders if order.seller.__class__.__name__ == 'Supplier')

    def calculate_profit(self) -> float:
        """Calculate profit (customer revenue - supplier costs)"""
        return self.total_customer_revenue() - self.total_supplier_costs()

    def get_customer_orders(self) -> List[Order]:
        """Get all customer orders"""
        return [order for order in self.orders if order.seller.__class__.__name__ == 'Warehouse']

    def get_supplier_orders(self) -> List[Order]:
        """Get all supplier orders"""
        return [order for order in self.orders if order.seller.__class__.__name__ == 'Supplier']

    def get_all_orders(self) -> List[Order]:
        """Get all orders (both customer and supplier)"""
        return self.orders

    def display_orders(self, orders: List[Order]):
        """Display orders in a formatted table"""
        print(f"{'Order ID':<10} {'Item':<15} {'Qty':<5} {'Total':<10} {'Buyer':<15} {'Seller':<15} {'Date'}")
        print("-" * 90)
        for order in orders:
            print(f"{order.order_id:<10} {order.item.name:<15} {order.quantity:<5} £{order.total_price:<8.2f} "
                  f"{getattr(order.buyer, 'name', 'N/A'):<15} {getattr(order.seller, 'name', 'N/A'):<15} "
                  f"{order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    def export_orders_to_csv(self, orders: List[Order], file_path: str):
        """Export orders to a CSV file"""
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Order ID", "Item", "Quantity", "Total Price", "Buyer", "Seller", "Date"])
            for order in orders:
                writer.writerow([
                    order.order_id,
                    order.item.name,
                    order.quantity,
                    f"£{order.total_price:.2f}",
                    getattr(order.buyer, 'name', 'N/A'),
                    getattr(order.seller, 'name', 'N/A'),
                    order.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                ])

    def _summarise_order(self, order) -> dict:
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
            "timestamp": order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def summarise_orders(self) -> list[dict]:
        """Summarize all orders in the system"""
        return [self._summarise_order(order) for order in self.orders]
