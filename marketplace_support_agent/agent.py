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
    check_return_eligibility,
    escalate_to_human,
    get_order_details,
    get_refund_status,
    get_store_policy,
    initiate_return,
    list_customer_orders,
    track_order,
)

MODEL = "gemini-2.5-flash"

order_agent = Agent(
    name="order_agent",
    model=MODEL,
    description=(
        "Handles order status, shipment tracking, expected delivery dates, "
        "and listing a customer's recent orders."
    ),
    instruction=prompts.ORDER_AGENT_INSTRUCTION,
    tools=[get_order_details, track_order, list_customer_orders],
)

returns_agent = Agent(
    name="returns_agent",
    model=MODEL,
    description=(
        "Handles returns, replacements, refund status, and order "
        "cancellations."
    ),
    instruction=prompts.RETURNS_AGENT_INSTRUCTION,
    tools=[
        check_return_eligibility,
        initiate_return,
        get_refund_status,
        cancel_order,
    ],
)

root_agent = Agent(
    name="marketplace_support",
    model=MODEL,
    description=(
        "Front-line marketplace customer support assistant that routes "
        "customers to order-tracking and returns specialists."
    ),
    instruction=prompts.COORDINATOR_INSTRUCTION,
    tools=[get_store_policy, escalate_to_human],
    sub_agents=[order_agent, returns_agent],
)
