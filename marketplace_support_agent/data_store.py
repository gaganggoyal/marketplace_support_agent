"""In-memory mock order database.

Stands in for real marketplace APIs (Amazon SP-API, Flipkart Seller API, etc.).
Dates are generated relative to today so return-window logic always demos well.
Replace the functions in tools/ with real API calls when going to production.
"""

from datetime import date, timedelta

TODAY = date.today()


def _d(days_ago: int) -> str:
    return (TODAY - timedelta(days=days_ago)).isoformat()


def _future(days_ahead: int) -> str:
    return (TODAY + timedelta(days=days_ahead)).isoformat()


# Keyed by order_id. One demo customer with orders across marketplaces.
ORDERS = {
    "AMZ-10041": {
        "order_id": "AMZ-10041",
        "marketplace": "Amazon",
        "customer_email": "demo.customer@example.com",
        "items": [
            {"name": "Sony WH-1000XM5 Headphones", "qty": 1, "price_inr": 26990}
        ],
        "amount_inr": 26990,
        "payment_method": "Credit Card",
        "status": "delivered",
        "order_date": _d(6),
        "delivered_date": _d(3),
        "return_window_days": 10,
        "tracking": [
            {"date": _d(6), "event": "Order placed"},
            {"date": _d(5), "event": "Shipped from seller facility, Mumbai"},
            {"date": _d(4), "event": "Out for delivery"},
            {"date": _d(3), "event": "Delivered - signed by resident"},
        ],
        "return": None,
    },
    "FLP-20017": {
        "order_id": "FLP-20017",
        "marketplace": "Flipkart",
        "customer_email": "demo.customer@example.com",
        "items": [
            {"name": "Puma Running Shoes (UK 9)", "qty": 1, "price_inr": 3499}
        ],
        "amount_inr": 3499,
        "current_price_inr": 2999,  # dropped after ordering — price-protection demo
        "payment_method": "UPI",
        "status": "shipped",
        "order_date": _d(2),
        "expected_delivery": _future(2),
        "return_window_days": 14,
        "tracking": [
            {"date": _d(2), "event": "Order placed"},
            {"date": _d(1), "event": "Packed at seller warehouse, Bengaluru"},
            {"date": _d(0), "event": "In transit - reached Delhi hub"},
        ],
        "return": None,
    },
    "AMZ-10087": {
        "order_id": "AMZ-10087",
        "marketplace": "Amazon",
        "customer_email": "demo.customer@example.com",
        "items": [
            {"name": "Prestige Induction Cooktop", "qty": 1, "price_inr": 2799},
            {"name": "Milton Casserole Set", "qty": 1, "price_inr": 1250},
        ],
        "amount_inr": 4049,
        "payment_method": "Cash on Delivery",
        "status": "processing",
        "order_date": _d(0),
        "expected_delivery": _future(4),
        "return_window_days": 7,
        "tracking": [{"date": _d(0), "event": "Order placed"}],
        "return": None,
    },
    "MYN-30112": {
        "order_id": "MYN-30112",
        "marketplace": "Myntra",
        "customer_email": "demo.customer@example.com",
        "items": [
            {"name": "Levi's 511 Jeans (32W)", "qty": 1, "price_inr": 2699}
        ],
        "amount_inr": 2699,
        "payment_method": "Credit Card",
        "status": "delivered",
        "order_date": _d(40),
        "delivered_date": _d(35),
        "return_window_days": 14,
        "tracking": [
            {"date": _d(40), "event": "Order placed"},
            {"date": _d(37), "event": "Shipped"},
            {"date": _d(35), "event": "Delivered"},
        ],
        "return": None,
    },
}

POLICIES = {
    "returns": (
        "Items can be returned within the return window shown on the order "
        "(typically 7-14 days from delivery, category dependent). Items must "
        "be unused with the BRAND packaging and tags intact; the outer "
        "shipping carton is not required. Pickup is scheduled free of charge "
        "within 24-48 hours of the return request."
    ),
    "refunds": (
        "Refunds always include the full amount paid, including shipping and "
        "handling fees, regardless of the return reason. Refunds go to the "
        "original payment method within 5-7 business days of the pickup "
        "scan; cash-on-delivery orders are refunded to the customer's choice "
        "of bank/UPI or wallet."
    ),
    "cancellations": (
        "Orders can be cancelled free of charge any time before they are "
        "shipped — instantly, with a full refund. Once shipped, the customer "
        "can refuse delivery at the door and the refund starts when the "
        "courier scans the returned package."
    ),
    "replacements": (
        "Damaged, defective, or wrong items are eligible for free replacement "
        "within the return window. If a replacement is out of stock, a full "
        "refund is issued instead."
    ),
    "warranty": (
        "Electronics carry the manufacturer's warranty (typically 1 year). "
        "After the marketplace return window closes, warranty claims are "
        "handled by authorised brand service centres; support shares the "
        "service-centre contacts and invoice, and steps in if the brand is "
        "unresponsive."
    ),
    "price-protection": (
        "If the price of an ordered item drops within 48 hours of placing "
        "the order, the difference is refunded on request after "
        "verification against price history."
    ),
}

# Demo customer account profile — in production this comes from the
# customer/risk platform.
ACCOUNT = {
    "customer_email": "demo.customer@example.com",
    "registered_phone_last4": "4242",
    "account_age_years": 15,
    "return_rate_percent": 4,
    "trusted": True,  # >1yr old, low return rate → instant-refund eligible
    "vip": True,  # high lifetime value → priority queues, same rules
    "goodwill_credits_this_quarter": 1,  # cap is 3 per quarter
    "returnless_replacements_this_month": 0,
    "orders_this_month": 6,
}

INVESTIGATIONS: dict[str, dict] = {}

_ticket_counter = 5000


def next_ticket_id() -> str:
    global _ticket_counter
    _ticket_counter += 1
    return f"TKT-{_ticket_counter}"


def next_case_id() -> str:
    global _ticket_counter
    _ticket_counter += 1
    return f"CASE-{_ticket_counter}"
