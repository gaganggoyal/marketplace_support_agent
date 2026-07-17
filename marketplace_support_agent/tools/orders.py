"""Order lookup and shipment tracking tools.

In production, replace the ORDERS dict access with calls to the marketplace
order APIs (Amazon SP-API getOrders, Flipkart Seller API, etc.).
"""

from ..data_store import ORDERS


def get_order_details(order_id: str) -> dict:
    """Fetch full details of an order: items, amount, payment method and status.

    Args:
        order_id: The order ID, e.g. "AMZ-10041" or "FLP-20017".

    Returns:
        A dict with the order details, or an error message if not found.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {
            "status": "error",
            "message": f"No order found with ID '{order_id}'. "
            "Please double-check the order ID.",
        }
    return {"status": "success", "order": order}


def track_order(order_id: str) -> dict:
    """Get the shipment tracking history and expected delivery date of an order.

    Args:
        order_id: The order ID to track.

    Returns:
        A dict with tracking events and delivery info, or an error message.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {
            "status": "error",
            "message": f"No order found with ID '{order_id}'.",
        }
    return {
        "status": "success",
        "order_id": order["order_id"],
        "current_status": order["status"],
        "tracking_events": order["tracking"],
        "expected_delivery": order.get("expected_delivery"),
        "delivered_date": order.get("delivered_date"),
    }


def list_customer_orders(customer_email: str) -> dict:
    """List recent orders placed by a customer, across all marketplaces.

    Args:
        customer_email: The email address the customer used to order.

    Returns:
        A dict with a summary list of the customer's orders.
    """
    email = customer_email.strip().lower()
    matches = [
        {
            "order_id": o["order_id"],
            "marketplace": o["marketplace"],
            "items": [i["name"] for i in o["items"]],
            "amount_inr": o["amount_inr"],
            "status": o["status"],
            "order_date": o["order_date"],
        }
        for o in ORDERS.values()
        if o["customer_email"] == email
    ]
    if not matches:
        return {
            "status": "error",
            "message": f"No orders found for {customer_email}.",
        }
    return {"status": "success", "orders": matches}
