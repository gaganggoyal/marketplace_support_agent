"""Price-protection tools (ruling 4.4: refund the difference within 48h)."""

from datetime import date

from ..data_store import ORDERS


def check_price_drop(order_id: str) -> dict:
    """Compare the price paid on an order with the item's current price and
    whether the order is within the 48-hour price-protection window.

    Args:
        order_id: The order to check.

    Returns:
        A dict with paid vs current price and window eligibility.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    current = order.get("current_price_inr", order["amount_inr"])
    days_since = (date.today() - date.fromisoformat(order["order_date"])).days
    within_window = days_since <= 2  # 48h, day-granular in the mock
    return {
        "status": "success",
        "paid_inr": order["amount_inr"],
        "current_price_inr": current,
        "difference_inr": max(order["amount_inr"] - current, 0),
        "within_48h_window": within_window,
        "eligible": within_window and current < order["amount_inr"],
    }


def refund_price_difference(order_id: str) -> dict:
    """Refund the price difference for an order whose price dropped within
    the 48-hour price-protection window. Policy entitlement — verified
    against price history, not goodwill.

    Args:
        order_id: The order to refund the difference for.

    Returns:
        A dict confirming the difference refund, or why it isn't eligible.
    """
    check = check_price_drop(order_id)
    if check["status"] == "error":
        return check
    if not check["eligible"]:
        reason = (
            "the order is outside the 48-hour price-protection window"
            if not check["within_48h_window"]
            else "the current price is not lower than what was paid"
        )
        return {"status": "error", "message": f"Not eligible: {reason}."}
    order = ORDERS[order_id.strip().upper()]
    diff = check["difference_inr"]
    order["price_difference_refunded_inr"] = diff
    return {
        "status": "success",
        "refunded_inr": diff,
        "message": f"₹{diff} price difference refunded to the original "
        "payment method within 5-7 business days.",
    }
