"""Identity-verification tests — the security-critical path.

Read-level verification gates access to another customer's order details, so
a false "verified: true" is an account-data leak. The original implementation
matched any input ending in the registered phone's last 4 digits, which let
an attacker (or a typo) pass with an unrelated number or the bare digits.
"""

from marketplace_support_agent.data_store import ACCOUNT
from marketplace_support_agent.tools import confirm_otp, verify_customer_contact

ORDER = "AMZ-10041"


def test_correct_email_verifies():
    assert verify_customer_contact(ORDER, "demo.customer@example.com")["verified"] is True


def test_correct_full_phone_verifies():
    assert verify_customer_contact(ORDER, ACCOUNT["registered_phone"])["verified"] is True


def test_full_phone_ignores_formatting():
    # spaces / +91 / dashes must not change the decision
    assert verify_customer_contact(ORDER, "+91 98123 04242")["verified"] is True


def test_unrelated_number_ending_in_last4_is_rejected():
    # 9999994242 ends in 4242 but is a different phone — must NOT verify
    assert verify_customer_contact(ORDER, "9999994242")["verified"] is False


def test_bare_last4_is_rejected():
    assert verify_customer_contact(ORDER, "4242")["verified"] is False


def test_arbitrary_string_ending_in_last4_is_rejected():
    assert verify_customer_contact(ORDER, "hacker4242")["verified"] is False


def test_empty_contact_is_rejected():
    assert verify_customer_contact(ORDER, "")["verified"] is False


def test_wrong_email_is_rejected():
    assert verify_customer_contact(ORDER, "someone.else@example.com")["verified"] is False


def test_unknown_order_errors():
    assert verify_customer_contact("FAKE-999", "demo.customer@example.com")["status"] == "error"


def test_confirm_otp_rejects_wrong_and_empty():
    assert confirm_otp(ORDER, "0000")["verified"] is False
    assert confirm_otp(ORDER, "")["verified"] is False
