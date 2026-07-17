"""Store policies, investigations, goodwill recommendations, escalation."""

from datetime import date, timedelta

from ..data_store import (
    ACCOUNT,
    INVESTIGATIONS,
    POLICIES,
    next_case_id,
    next_ticket_id,
)

# Investigation types and their resolution timelines (director's rulings
# 1.1, 1.4, 1.5, 2.3, 2.4, 2.5, 2.8, 6.3).
INVESTIGATION_TYPES = {
    "courier_dnr": {"days": 2, "team": "logistics"},
    "third_party_delivery": {"days": 2, "team": "logistics"},
    "packing_check": {"days": 2, "team": "fulfilment"},
    "high_value_claim": {"days": 5, "team": "claims"},
    "counterfeit": {"days": 5, "team": "category"},
    "damaged_nonreturnable": {"days": 2, "team": "claims"},
}


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
    if ACCOUNT.get("vip"):
        priority = "high"  # ruling 9.4: same rules, faster queue
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


def open_investigation(order_id: str, investigation_type: str, summary: str) -> dict:
    """Open an internal investigation case and give the customer a case ID
    and resolution timeline.

    Use for: courier_dnr (package marked delivered but not received),
    third_party_delivery (handed to neighbour/security, missing),
    packing_check (item missing from box / wrong item / missing freebie),
    high_value_claim (empty box or swapped contents on expensive items),
    counterfeit (fake product claims, after customer evidence collected),
    damaged_nonreturnable (damaged item in a non-returnable category
    above Rs 1000).

    Args:
        order_id: The order under investigation.
        investigation_type: One of courier_dnr, third_party_delivery,
            packing_check, high_value_claim, counterfeit,
            damaged_nonreturnable.
        summary: What the customer reported and any evidence provided.

    Returns:
        A dict with the case ID, owning team, and resolution deadline.
    """
    kind = INVESTIGATION_TYPES.get(investigation_type)
    if not kind:
        return {
            "status": "error",
            "message": f"Unknown investigation type '{investigation_type}'.",
            "available_types": sorted(INVESTIGATION_TYPES),
        }
    case_id = next_case_id()
    deadline = (date.today() + timedelta(days=kind["days"])).isoformat()
    INVESTIGATIONS[case_id] = {
        "case_id": case_id,
        "order_id": order_id.strip().upper(),
        "type": investigation_type,
        "team": kind["team"],
        "summary": summary,
        "resolution_deadline": deadline,
        "state": "open",
    }
    return {
        "status": "success",
        "case_id": case_id,
        "team": kind["team"],
        "resolution_deadline": deadline,
        "message": f"Case {case_id} opened with the {kind['team']} team. "
        f"Resolution by {deadline}.",
    }


def recommend_goodwill(order_id: str, reason: str, suggested_voucher_inr: int) -> dict:
    """Recommend a goodwill voucher for HUMAN approval. The agent can never
    issue goodwill itself (Rs 0 autonomy). Enforces the farming cap: max 3
    goodwill credits per account per quarter.

    Args:
        order_id: The order the goodwill relates to.
        reason: Why goodwill is deserved (what failure the customer suffered).
        suggested_voucher_inr: The voucher amount to suggest to the approver.

    Returns:
        A dict with the recommendation ticket, or a suppression notice when
        the account is over the quarterly cap.
    """
    used = ACCOUNT["goodwill_credits_this_quarter"]
    if used >= 3:
        ticket_id = next_ticket_id()
        return {
            "status": "success",
            "outcome": "suppressed_over_cap",
            "ticket_id": ticket_id,
            "message": f"Account already has {used} goodwill credits this "
            f"quarter (cap 3). Recommendation suppressed; case {ticket_id} "
            "routed to human review with a farming note. Do not promise "
            "the customer any compensation.",
        }
    ticket_id = next_ticket_id()
    return {
        "status": "success",
        "outcome": "recommended",
        "ticket_id": ticket_id,
        "form": "voucher",
        "suggested_voucher_inr": suggested_voucher_inr,
        "message": f"Goodwill recommendation {ticket_id} created for human "
        "approval (voucher). Tell the customer the team will review and "
        "confirm — do not promise the amount.",
    }
