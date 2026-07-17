"""Returns, refunds, replacements and cancellation tools."""

from datetime import date, timedelta

from ..data_store import ORDERS, next_ticket_id


def check_return_eligibility(order_id: str) -> dict:
    """Check whether an order is still within its return window.

    Args:
        order_id: The order ID to check.

    Returns:
        A dict saying whether the order is eligible for return and until when.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    if order["status"] == "cancelled":
        return {"status": "success", "eligible": False, "reason": "Order was cancelled."}
    if order["status"] != "delivered":
        return {
            "status": "success",
            "eligible": False,
            "reason": "Order has not been delivered yet. It can be returned "
            "after delivery, or refused at the doorstep.",
        }
    delivered = date.fromisoformat(order["delivered_date"])
    deadline = delivered + timedelta(days=order["return_window_days"])
    eligible = date.today() <= deadline
    return {
        "status": "success",
        "eligible": eligible,
        "return_window_days": order["return_window_days"],
        "delivered_date": order["delivered_date"],
        "return_deadline": deadline.isoformat(),
        "reason": None if eligible else "The return window has closed.",
    }


def initiate_return(order_id: str, reason: str, resolution: str) -> dict:
    """Start a return for a delivered order and schedule a pickup.

    Args:
        order_id: The order ID to return.
        reason: Why the customer wants to return (e.g. "size too small",
            "damaged on arrival", "not as described").
        resolution: What the customer wants - "refund" or "replacement".

    Returns:
        A dict with the return ID and pickup date, or an error message.
    """
    eligibility = check_return_eligibility(order_id)
    if eligibility["status"] == "error":
        return eligibility
    if not eligibility["eligible"]:
        return {
            "status": "error",
            "message": f"Return not possible: {eligibility['reason']}",
        }
    if resolution not in ("refund", "replacement"):
        return {
            "status": "error",
            "message": "resolution must be 'refund' or 'replacement'.",
        }
    order = ORDERS[order_id.strip().upper()]
    if order.get("return"):
        return {
            "status": "error",
            "message": f"A return already exists for this order: "
            f"{order['return']['return_id']}",
        }
    pickup = (date.today() + timedelta(days=2)).isoformat()
    return_id = f"RET-{next_ticket_id().split('-')[1]}"
    order["return"] = {
        "return_id": return_id,
        "reason": reason,
        "resolution": resolution,
        "pickup_date": pickup,
        "refund_status": "pending_pickup" if resolution == "refund" else None,
    }
    return {
        "status": "success",
        "return_id": return_id,
        "resolution": resolution,
        "pickup_date": pickup,
        "message": "Pickup scheduled. Keep the item unused with original "
        "packaging and tags for the pickup agent.",
    }


def get_refund_status(order_id: str) -> dict:
    """Check the refund status for an order that has a return in progress.

    Args:
        order_id: The order ID whose refund to check.

    Returns:
        A dict with the refund stage and expected credit timeline.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    ret = order.get("return")
    if not ret:
        return {
            "status": "error",
            "message": "No return or refund is in progress for this order.",
        }
    return {
        "status": "success",
        "return_id": ret["return_id"],
        "resolution": ret["resolution"],
        "refund_status": ret.get("refund_status", "not_applicable"),
        "pickup_date": ret["pickup_date"],
        "note": "Refunds are credited to the original payment method within "
        "5-7 business days after the item passes quality check.",
    }


def cancel_order(order_id: str) -> dict:
    """Cancel an order that has not been shipped yet.

    Args:
        order_id: The order ID to cancel.

    Returns:
        A dict confirming the cancellation, or explaining why it isn't possible.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    if order["status"] in ("shipped", "delivered"):
        return {
            "status": "error",
            "message": f"Order is already {order['status']} and can no longer "
            "be cancelled. A return can be requested after delivery instead.",
        }
    if order["status"] == "cancelled":
        return {"status": "error", "message": "This order is already cancelled."}
    order["status"] = "cancelled"
    refund_note = (
        "No amount was charged (Cash on Delivery)."
        if order["payment_method"] == "Cash on Delivery"
        else "The amount will be refunded to the original payment method "
        "within 5-7 business days."
    )
    return {
        "status": "success",
        "order_id": order["order_id"],
        "message": f"Order cancelled successfully. {refund_note}",
    }
