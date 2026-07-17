# Marketplace Support Agent

A customer-support agent for e-commerce marketplaces (Amazon/Flipkart style),
built with Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
and deployable to Vertex AI Agent Engine.

## Architecture

```
marketplace_support (coordinator)
├── tools: get_store_policy, escalate_to_human
├── order_agent      — order details, tracking, list customer orders
└── returns_agent    — return eligibility, returns/replacements,
                       refund status, cancellations
```

Orders live in a mock in-memory store ([data_store.py](marketplace_support_agent/data_store.py))
so the whole flow works locally. Swap the tool bodies in
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

Then put the same project ID into `marketplace_support_agent/.env`
(`GOOGLE_CLOUD_PROJECT=...`).

## Run locally

```bash
source .venv/bin/activate
adk web          # browser chat UI at http://localhost:8000
# or
adk run marketplace_support_agent   # chat in the terminal
```

Demo data to try (customer email `demo.customer@example.com`):

| Order | Marketplace | Status | Good for testing |
|---|---|---|---|
| AMZ-10041 | Amazon | delivered 3 days ago | returns/refunds |
| FLP-20017 | Flipkart | shipped, in transit | tracking, cancel-after-ship |
| AMZ-10087 | Amazon | processing (COD) | cancellation |
| MYN-30112 | Myntra | delivered 35 days ago | return window expired |

Example prompts:
- "Where is my order FLP-20017?"
- "The headphones from AMZ-10041 are defective, I want my money back"
- "Cancel AMZ-10087"
- "What's your refund policy?"
- "I want to talk to a human"

## Deploy to Google Cloud (Agent Engine)

```bash
./deploy.sh
```

After deployment the agent appears under **Agent Platform → Agent Engine**
in the Cloud Console, where you can test it and wire it to channels.

## Project layout

```
marketplace_support_agent/        # ADK agent package
├── agent.py                      # root_agent + sub-agents
├── prompts.py                    # agent instructions
├── data_store.py                 # mock order database
├── tools/
│   ├── orders.py                 # get_order_details, track_order, list_customer_orders
│   ├── returns.py                # eligibility, initiate_return, refund status, cancel
│   └── support.py                # policies, escalate_to_human
└── .env                          # Vertex AI project config
```
