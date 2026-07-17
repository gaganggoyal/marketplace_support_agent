"""Tiered identity verification (ruling 10.1).

Read access: registered email/phone must match the order.
Money-moving or account changes: OTP verification.
Mock implementation — in production this calls the identity platform.
"""

from ..data_store import ACCOUNT, ORDERS

DEMO_OTP = "4242"


def verify_customer_contact(order_id: str, email_or_phone: str) -> dict:
    """Verify the customer's email or phone matches the order, allowing order
    details to be shared (read-level verification).

    Args:
        order_id: The order being discussed.
        email_or_phone: The email address or phone number the customer says
            is registered on the account.

    Returns:
        A dict with verified true/false.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    given = email_or_phone.strip().lower()
    matches = given == order["customer_email"] or given.endswith(
        ACCOUNT["registered_phone_last4"]
    )
    return {
        "status": "success",
        "verified": matches,
        "message": "Contact matches the order."
        if matches
        else "That contact does not match this order's records.",
    }


def request_otp(order_id: str) -> dict:
    """Send an OTP to the customer's registered phone before a money-moving
    or account-changing action (prepaid cancellation, refund destination or
    address change).

    Args:
        order_id: The order the sensitive action applies to.

    Returns:
        A dict confirming where the OTP was sent.
    """
    order = ORDERS.get(order_id.strip().upper())
    if not order:
        return {"status": "error", "message": f"No order found with ID '{order_id}'."}
    return {
        "status": "success",
        "message": "OTP sent to the registered mobile number ending "
        f"{ACCOUNT['registered_phone_last4']}.",
        "demo_note": f"(Local demo only: the OTP is {DEMO_OTP}.)",
    }


def confirm_otp(order_id: str, otp: str) -> dict:
    """Check the OTP the customer provided.

    Args:
        order_id: The order the sensitive action applies to.
        otp: The code the customer typed.

    Returns:
        A dict with verified true/false.
    """
    ok = otp.strip() == DEMO_OTP
    return {
        "status": "success",
        "verified": ok,
        "message": "OTP verified." if ok else "Incorrect OTP. One retry allowed, "
        "then the action must go through human support.",
    }
