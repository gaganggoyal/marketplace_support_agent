#!/usr/bin/env bash
# Deploy the agent to Vertex AI Agent Engine.
# Prerequisites: gcloud auth done, project set in marketplace_support_agent/.env
set -euo pipefail
cd "$(dirname "$0")"

source .venv/bin/activate
adk deploy agent_engine \
  --display_name "marketplace-support-agent" \
  marketplace_support_agent
