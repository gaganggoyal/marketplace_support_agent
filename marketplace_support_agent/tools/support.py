"""Store policies and human escalation tools."""

from ..data_store import POLICIES, next_ticket_id


def get_store_policy(topic: str) -> dict:
    """Look up the store policy on a topic.

    Args:
        topic: One of "returns", "refunds", "cancellations", "replacements",
            "warranty".

    Returns:
        A dict with the policy text, or the list of available topics.
    """
    policy = POLICIES.get(topic.strip().lower())
    if not policy:
        return {
            "status": "error",
            "message": f"No policy found for '{topic}'.",
            "available_topics": sorted(POLICIES),
        }
    return {"status": "success", "topic": topic, "policy": policy}


def escalate_to_human(issue_summary: str, priority: str) -> dict:
    """Create a support ticket and hand the case to a human agent.

    Use when the customer explicitly asks for a human, is upset after a failed
    resolution, or the issue is outside what the available tools can solve
    (payment disputes, account compromise, legal complaints).

    Args:
        issue_summary: A concise summary of the customer's issue and what has
            been tried so far.
        priority: "low", "medium", or "high". Use "high" for payment issues,
            suspected fraud, or very upset customers.

    Returns:
        A dict with the ticket ID and expected response time.
    """
    if priority not in ("low", "medium", "high"):
        priority = "medium"
    ticket_id = next_ticket_id()
    response_time = {"high": "2 hours", "medium": "12 hours", "low": "24 hours"}[
        priority
    ]
    # In production: create the ticket in Zendesk/Freshdesk/Salesforce here.
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "priority": priority,
        "expected_response_time": response_time,
        "message": f"Ticket {ticket_id} created. A human support specialist "
        f"will reach out within {response_time}.",
    }
