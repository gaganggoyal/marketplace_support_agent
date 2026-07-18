"""Returns, refunds, cancellations, and state-transition guards."""

from marketplace_support_agent.tools import (
    cancel_order,
    check_return_eligibility,
    get_refund_status,
    initiate_return,
)


def test_return_rejected_before_delivery():
    # AMZ-10087 is still processing
    result = initiate_return("AMZ-10087", "changed mind", "refund")
    assert result["status"] == "error"


def test_return_rejected_bad_resolution():
    result = initiate_return("AMZ-10041", "damaged", "store credit")
    assert result["status"] == "error"


def test_return_rejected_outside_window():
    # MYN-30112 was delivered 35 days ago, window is 14 days
    result = check_return_eligibility("MYN-30112")
    assert result["eligible"] is False


def test_double_return_is_blocked():
    first = initiate_return("AMZ-10041", "defective", "replacement")
    assert first["status"] == "success"
    second = initiate_return("AMZ-10041", "defective", "replacement")
    assert second["status"] == "error"


def test_refund_status_requires_a_return():
    assert get_refund_status("AMZ-10041")["status"] == "error"


def test_cannot_cancel_shipped_order():
    # FLP-20017 is shipped
    assert cancel_order("FLP-20017")["status"] == "error"


def test_cancel_then_cancel_again_is_blocked():
    first = cancel_order("AMZ-10087")
    second = cancel_order("AMZ-10087")
    assert first["status"] == "success"
    assert second["status"] == "error"


def test_unknown_order_errors_everywhere():
    assert check_return_eligibility("NOPE-1")["status"] == "error"
    assert initiate_return("NOPE-1", "x", "refund")["status"] == "error"
    assert cancel_order("NOPE-1")["status"] == "error"
