"""Marketplace customer support agent.

A coordinator agent routes conversations to two specialists:
- order_agent: order status, tracking, delivery questions
- returns_agent: returns, refunds, replacements, cancellations

Run locally with `adk web` (from the parent directory) or `adk run
marketplace_support_agent`. Deploy with `adk deploy agent_engine`.
"""

from google.adk.agents import Agent

from . import prompts
from .tools import (
    cancel_order,
    check_price_drop,
    check_return_eligibility,
    confirm_otp,
    escalate_to_human,
    get_order_details,
    get_refund_status,
    get_store_policy,
    initiate_return,
    list_customer_orders,
    open_investigation,
    recommend_goodwill,
    refund_price_difference,
    request_otp,
    track_order,
    verify_customer_contact,
)

MODEL = "gemini-2.5-flash"

# Every agent can verify identity and escalate.
COMMON_TOOLS = [verify_customer_contact, request_otp, confirm_otp, escalate_to_human]

order_agent = Agent(
    name="order_agent",
    model=MODEL,
    description=(
        "Handles order status, shipment tracking, delivery problems "
        "(not received, late, tampered), and listing a customer's orders."
    ),
    instruction=prompts.ORDER_AGENT_INSTRUCTION,
    tools=[
        get_order_details,
        track_order,
        list_customer_orders,
        open_investigation,
        *COMMON_TOOLS,
    ],
)

returns_agent = Agent(
    name="returns_agent",
    model=MODEL,
    description=(
        "Handles returns, replacements, refund status, cancellations, "
        "price-drop refunds, and product quality/warranty issues."
    ),
    instruction=prompts.RETURNS_AGENT_INSTRUCTION,
    tools=[
        check_return_eligibility,
        initiate_return,
        get_refund_status,
        cancel_order,
        check_price_drop,
        refund_price_difference,
        open_investigation,
        recommend_goodwill,
        *COMMON_TOOLS,
    ],
)

root_agent = Agent(
    name="marketplace_support",
    model=MODEL,
    description=(
        "Front-line marketplace customer support assistant: routes to "
        "order-tracking and returns specialists, and itself handles "
        "billing, payments, account security, and safety incidents."
    ),
    instruction=prompts.COORDINATOR_INSTRUCTION,
    tools=[get_store_policy, recommend_goodwill, *COMMON_TOOLS],
    sub_agents=[order_agent, returns_agent],
)
