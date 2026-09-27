# Marketplace Support Agent

[![CI](https://github.com/gaganggoyal/marketplace_support_agent/actions/workflows/ci.yml/badge.svg)](https://github.com/gaganggoyal/marketplace_support_agent/actions/workflows/ci.yml)
[![Python 3.10–3.12](https://img.shields.io/badge/python-3.10%E2%80%933.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A customer-support agent for e-commerce marketplaces (Amazon/Flipkart style),
built with Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
and deployable to Vertex AI Agent Engine.

Its behaviour is not generic: it runs a **73-ruling support playbook** built
through an interactive training session between a support-director persona
and a customer with 15 years of daily marketplace ordering experience. Every
rule in [prompts.py](marketplace_support_agent/prompts.py) traces to a
numbered ruling in [TRAINING_DECISIONS.md](TRAINING_DECISIONS.md) (the full
questionnaire is in [TRAINING_QUESTIONNAIRE.md](TRAINING_QUESTIONNAIRE.md)).

## Architecture

```
marketplace_support (coordinator)
│  policies · billing & payments · account security · safety incidents
│  goodwill recommendations · escalation
├── order_agent      — tracking, delivery failures (DNR, tampered, late),
│                      delivery investigations
└── returns_agent    — returns/replacements, refunds, cancellations,
                       price protection, quality & warranty
```

All agents share: tiered identity verification (contact match to read,
OTP to change), language preference, escalation triggers, and a strict
never-reveal list.

## The playbook's signature rules

- **₹0 money autonomy** — the AI never issues compensation; it *recommends*
  a voucher (`recommend_goodwill`) and a human approves. Farming cap of 3
  goodwill credits per account per quarter is enforced in code.
- **Investigate first, then be generous** — every loss/damage claim (not
  received, missing item, wrong item, empty box) opens a tracked
  investigation with a case ID and deadline before any refund.
- **All fees always refunded** — shipping/handling included, even on
  change-of-mind returns.
- **48-hour price protection** — price drops after ordering refund the
  difference, verified against price history.
- **Brand packaging only** — returns need the brand box/tags, not the
  shipping carton.
- **Human-only actions** — account deletion, phone re-binding, fraud-flag
  overrides, out-of-window exceptions, and anything in a safety incident.

## Tools (16)

| Area | Tools |
|---|---|
| Orders | `get_order_details`, `track_order`, `list_customer_orders` |
| Returns | `check_return_eligibility`, `initiate_return`, `get_refund_status`, `cancel_order` |
| Price protection | `check_price_drop`, `refund_price_difference` |
| Investigations | `open_investigation` (6 case types with timelines) |
| Goodwill | `recommend_goodwill` (human-approved, capped) |
| Identity | `verify_customer_contact`, `request_otp`, `confirm_otp` |
| Support | `get_store_policy`, `escalate_to_human` |

Orders live in a mock in-memory store
([data_store.py](marketplace_support_agent/data_store.py)) so the whole flow
works locally. Swap the tool bodies in
[tools/](marketplace_support_agent/tools/) for real marketplace APIs
(Amazon SP-API, Flipkart Seller API, Zendesk, etc.) when going live.

## One-time Google Cloud setup

```bash
# 1. Log in (opens a browser)
gcloud auth login
gcloud auth application-default login

# 2. Point at your project (ID from the Cloud Console project picker)
gcloud config set project YOUR_PROJECT_ID

# 3. Enable the Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

Then copy `marketplace_support_agent/.env.example` to
`marketplace_support_agent/.env` and set the same project ID.

## Run locally

```bash
source .venv/bin/activate
adk web          # browser chat UI at http://localhost:8000
# or
adk run marketplace_support_agent   # chat in the terminal
```

Demo data (customer email `demo.customer@example.com`, demo OTP `4242`):

| Order | Marketplace | Status | Good for testing |
|---|---|---|---|
| AMZ-10041 | Amazon | delivered 3 days ago | returns, refunds, DNR investigation |
| FLP-20017 | Flipkart | shipped, price dropped ₹500 | tracking, price protection, cancel-after-ship |
| AMZ-10087 | Amazon | processing (COD) | frictionless cancellation |
| MYN-30112 | Myntra | delivered 35 days ago | window expired → warranty routing |

Prompts that exercise the playbook:
- "Where is my order FLP-20017?"
- "FLP-20017 price dropped after I ordered — I want the difference" *(should refund ₹500)*
- "My AMZ-10041 package shows delivered but I never got it" *(should open an investigation, not refund)*
- "Give me a voucher for the late delivery" *(should apologise, not pay)*
- "Cancel AMZ-10087" / "What's your refund policy?" / "I want a human"

## Tested — including the security path

```bash
pip install -r requirements-dev.txt
pytest
```

Identity verification gates access to another customer's order details, so I
attacked it directly. The original contact check matched any input ending in
the registered phone's last 4 digits — an **identity-verification bypass**
that's now fixed and locked down by tests
([tests/test_verification.py](tests/test_verification.py)):

| Input | Before | Now |
|---|---|---|
| `9999994242` (unrelated number ending 4242) | ✅ verified — **account-data leak** | ❌ rejected |
| `hacker4242` (arbitrary string ending 4242) | ✅ verified | ❌ rejected |
| `4242` (the bare last-4) | ✅ verified | ❌ rejected |
| `demo.customer@example.com` (real email) | ✅ verified | ✅ verified |
| `+91 98123 04242` (real full phone, any formatting) | — | ✅ verified |

Verification now requires the **full** registered phone (digits compared,
formatting ignored) or an exact email match. The rest of the suite covers
returns/refunds/cancellation state transitions — no return before delivery,
no double return, no cancelling a shipped order, refund-status needs a
return — against a store reset to clean seed data before every test.

## Deploy to Google Cloud (Agent Engine)

```bash
./deploy.sh
```

After deployment the agent appears under **Agent Platform → Agent Engine**
in the Cloud Console, where you can test it and wire it to channels.

## Project layout

```
marketplace_support_agent/        # ADK agent package
├── agent.py                      # root_agent + sub-agents + tool wiring
├── prompts.py                    # playbooks (every rule tagged [ruling #])
├── data_store.py                 # mock orders, account profile, policies
├── tools/
│   ├── orders.py                 # lookups & tracking
│   ├── returns.py                # eligibility, returns, refunds, cancel
│   ├── pricing.py                # 48h price protection
│   ├── verification.py           # contact match + OTP (demo: 4242)
│   └── support.py                # policies, investigations, goodwill, escalation
├── .env.example                  # Vertex AI config template
tests/                            # tool tests, incl. the identity-verification suite
TRAINING_QUESTIONNAIRE.md         # the 73 scenarios
TRAINING_DECISIONS.md             # the 73 rulings (source of truth)
LICENSE                           # MIT
.github/workflows/ci.yml          # runs the suite on every push
deploy.sh                         # adk deploy agent_engine
```

## Who decided all this

I went through all 73 scenarios in
[TRAINING_QUESTIONNAIRE.md](TRAINING_QUESTIONNAIRE.md) as someone who has
ordered from these marketplaces nearly every day for 15 years, and ruled on
each one. The rulings that define this agent:

- **₹0 money autonomy.** The agent never hands out compensation on its own.
  It can only recommend goodwill and a human approves; the 3-per-quarter
  farming cap is enforced in code, not in the prompt.
- **Investigate first, then be generous.** Every loss claim opens a tracked
  case with an ID and a deadline before any refund, because instant refunds
  train fraudsters faster than they win customers.
- **All fees always refunded** and **48-hour price protection**: the two
  policies that made me loyal to the platforms that offer them.

Every rule in [prompts.py](marketplace_support_agent/prompts.py) carries its
ruling number, so any behaviour can be traced back to the decision behind it.

---

**Gagandeep Goyal** — e-commerce operator (10+ years), building AI agents on
Google's ADK. Portfolio: [gagan.indiaoffers.in](https://gagan.indiaoffers.in)
· GitHub: [@gaganggoyal](https://github.com/gaganggoyal)
