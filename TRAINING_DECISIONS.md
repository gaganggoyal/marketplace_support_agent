# Training Decisions (Director's Rulings)

Running log of answers from the training questionnaire. These get encoded
into `prompts.py` playbooks and tools. ✏️ = user overrode the default.

## Section 9 — Compensation & Goodwill
- **9.1 AI goodwill cap: ₹0** ✏️ — the AI never issues compensation itself.
  It assesses eligibility and *recommends* an amount in the escalation ticket;
  a human approves and issues. (Default was ₹500 — user chose stricter.)

## Section 10 — Guardrails & Identity
- **10.2 Human-only actions: all six** — refunds above cap outside return
  flow, account deletion, phone/email re-binding, fraud-flag overrides,
  warranty exceptions past window, safety incidents.
- **10.1 Verification: tiered** — order ID + registered email/phone match to
  view details; OTP for money-moving/account changes.
- **10.3 AI disclosure: only if asked** ✏️ — no proactive "I'm an AI" in the
  greeting; answer honestly if the customer asks. (Default was always-disclose.)
- **10.4 Language: ask preference once** ✏️ — one-time "Hindi ya English?"
  at session start, then stick to it. (Default was mirror-the-customer.)
- **10.5 Auto-escalation triggers: all five** — 3+ unresolved turns, high
  frustration, legal/safety/fraud keywords, evidence disputes, third contact
  on same issue.
- **10.6 Never reveal: all five** — other customers' data, fraud flags &
  thresholds, seller cost data, courier employee details, and never hint at
  policy exceptions before the case qualifies.

## Section 1 — Delivery & WISMO
- **1.1 DNR (marked delivered, not received): check-and-wait for ALL
  values** ✏️ — ask customer to check household/neighbours/security, open
  courier investigation, resolve (refund/replace) within 48h. No instant
  refunds even for low value. (Default was value-tiered.)
- **1.2 Late in transit: proactive at +3 days past ETA** — offer choice:
  keep waiting (delay escalated to logistics) or cancel for full refund.
- **1.3 "Out for delivery" loop (3 days): escalate to logistics only** ✏️ —
  push courier for a firm date; offer refund only if the customer asks.
  (Default also proactively offered refund.)
- **1.4 Handed to neighbour/security without consent, now missing:
  split** ✏️ — investigate the courier, resolve via HUMAN-APPROVED goodwill
  rather than automatic full liability. (Default was full DNR liability.)
- **1.5 Item missing from multi-item box: investigate first, always** ✏️ —
  packing-station weight-log check for every claim regardless of value,
  resolve within 48h. (Default was value-tiered.)
- **1.6 Tampered/empty package: split by moment** — refused at doorstep →
  auto-refund on RTO scan; accepted then reported within 24h → photo
  evidence + quick human review, then refund. Agent always advises
  customers to refuse tampered packages.
- **1.7 Courier misconduct (demanded cash / rude): apology + complaint log
  only** ✏️ — conduct report to logistics partner, no compensation.
  (Default was to also recommend goodwill to a human.)
- **1.8 Address change after shipping: redirect + hub-hold options** ✏️ —
  offer courier redirect where supported OR hold at courier hub for
  self-pickup; fallback is refuse-at-door → refund → reorder. (Default was
  redirect-only with no-promise framing.)
- **1.9 Travelling customer, wants hold/reschedule: courier's standard flow
  only** ✏️ — point them to the courier's own reschedule link/app; agent
  doesn't intervene. (Default was agent-managed reschedule window.)
- **1.10 Heavy-item carry request beyond doorstep: check paid-assist,
  honest expectations** — log request with logistics for paid/partner
  assist where available; if unavailable, say so honestly, suggest local
  help. Never flatly refuse.

## Section 2 — Returns & Replacements
- **2.1 Defective but window closed: always route to brand warranty** ✏️ —
  provide service-centre contacts + invoice, regardless of how recently
  the window closed. No marketplace exceptions. (Default allowed a
  human-approved exception ≤7 days past window.)
- **2.2 Change-of-mind after window: polite firm refusal** — empathetic no,
  explain the window, no goodwill.
- **2.3 Wrong item received: investigate first** ✏️ — verify packing
  records (24–48h) before shipping replacement or refunding. (Default was
  immediate priority replacement.)
- **2.4 High-value empty-box/brick claim: structured investigation,
  3–5 days** — weight logs, CCTV, serial checks; human decides. Customer
  gets case ID + timeline upfront. Never accuse, never instant-refund.
- **2.5 Counterfeit claim: evidence → category-team investigation** ✏️ —
  ask customer for screenshots/photos evidencing the fake; raise an
  investigation with the relevant category team; if genuine → arrange
  pickup and refund OR replacement, customer's preference. (Default was
  immediate refund + seller flag without evidence gate.)
- **2.6 Size exchange: true exchange, price held** — new size ships on
  pickup scan of the old; customer keeps their original price.
- **2.7 Used/worn return ("didn't fit", tags missing): refuse + email
  second chance, value-aware** ✏️ — if courier already rejected at
  doorstep for missing tags: polite refusal quoting policy, BUT offer a
  second chance — customer emails product photos (both sides) to support
  for one human re-review, while being told honestly it will most likely
  be rejected. If item price > ₹2,000, the agent proactively encourages
  the email-with-photos human review — rationale: scammers don't run this
  play on high-cost items, so expensive disputes are more likely genuine.
- **2.8 Non-returnable category arrives damaged: returnless replacement
  with abuse counter** ✏️ — require photo proof of damage/defect →
  arrange replacement, customer KEEPS the damaged item (no pickup). Each
  such case increments a per-customer, per-category returnless counter;
  BLOCK that category for the customer if returnless replacements/refunds
  exceed 10% of their total orders per month. If item price > ₹1,000:
  raise an investigation BEFORE any resolution.
- **2.9 Pickup failed repeatedly: escalate at 2nd failure; at 3rd failure
  refund without pickup if item ≤ ₹800** — above ₹800: priority pickup
  with a named window. (Return-flow refund, so allowed despite ₹0
  goodwill autonomy.)
- **2.10 Doorstep QC rejection disputed: one email appeal with photos**
  (the 2.7 rule) — both-side photos to support email → one human
  re-review → possible pickup override; honest expectation-setting;
  proactively encouraged for items > ₹2,000.
- **2.11 Packaging rule: BRAND packaging required, outer packing material
  optional** ✏️ — the product's own brand box/tags must be present; the
  shipping carton or other material is not mandatory.
- **2.12 Serial mismatch on returned electronics: reject with evidence +
  dispute path + account flag** — no refund; show shipped-vs-received
  serial evidence, offer formal dispute path (protects against warehouse
  error), flag the account. Never use the word "fraud" with the customer.

## Section 3 — Refunds
- **3.1 Refund past promise: ARN + 48h re-promise + auto-escalate** —
  apologise, share bank reference (ARN), re-promise 48h, auto-escalate to
  payments if missed again. Never open with "check with your bank".
- **3.2 Refund to closed card: proactive re-route with tracking** —
  explain 7–14 day bank bounce, re-issue to customer's chosen destination
  the moment it returns, case ID issued so it can't be forgotten.
- **3.3 COD refunds: customer chooses bank/UPI or wallet** — wallet only
  ever as opt-in, never forced.
- **3.4 Keep-item + partial refund: only when the CUSTOMER suggests it** ✏️
  — the agent never introduces the idea (prevents partial-refund fishing);
  if the customer proposes it, route to human review. (Default let the
  agent propose it.)
- **3.5 Payment deducted, no order created: reassure — money never reached
  us** ✏️ — explain that in payment failures the amount stays with the
  bank and auto-reverses within a MAXIMUM of 15 days; nothing for the
  customer to do but wait; if it misses that window, come back and we'll
  guide them — warm framing ("we're always here to help"). (Default was
  5–7 day framing + day-7 gateway dispute escalation.)
- **3.6 Fee deductions on refunds: ALWAYS refund everything** ✏️ — all
  shipping/handling fees refunded regardless of return reason, including
  change-of-mind. (Default was fault-based deduction.)
- **3.7 Instant refunds: trusted accounts (>1yr, low return rate) get
  refund-on-pickup-scan up to ₹2,000** — everyone else refunds after
  pickup scan; full-QC wait only for flagged accounts.
- **3.8 Refund-delay compensation demands: apology only, never
  compensation** ✏️ — sincere apology + explanation; delay compensation
  is not offered. (Default was human-reviewed goodwill recommendation.)

## Section 4 — Cancellations
- **4.1 Cancel while processing: frictionless** — one "are you sure?",
  instant cancel, full refund to source, NO retention pitch.
- **4.2 Cancel after shipped: refuse-at-door → refund on RTO scan** —
  timeline expectation set upfront; no interception promises.
- **4.3 Seller/marketplace cancelled unilaterally: full instant refund +
  human-approved goodwill recommendation + agent actively helps find an
  alternative at similar price.**
- **4.4 Price drop after ordering: REFUND THE DIFFERENCE** ✏️ — true
  price protection within 24–48h of ordering; the agent verifies the drop
  from price history and processes the difference refund as policy (an
  entitlement, not goodwill, so it doesn't hit the ₹0-autonomy rule).
  (Default was cancel-and-reorder only.)
- **4.5 Partial cancel of packed multi-item order: deliver all +
  pre-created return** — honest "can't unpack the shipment" framing;
  pickup for the unwanted item auto-created; refund on pickup scan.

## Section 5 — Payments, Pricing & Billing
- **5.1 No-cost EMI interest complaint: explain mechanics, fix if discount
  missing** — verify the invoice discount; if absent → billing-error
  escalation + interest amount credited.
- **5.2 Split-payment refund: each source refunds to itself** — gift card
  → gift card, card → card; extend gift-card expiry if the refund lands
  near it.
- **5.3 Missing cashback: verify offer terms → manual credit + batch
  flag** — if eligible, escalate for manual credit AND flag possible
  batch failure; if ineligible, explain exactly which condition failed.
- **5.4 Promo code failed at checkout: verifiable log error → credit the
  difference (human approves)** — otherwise polite refusal + working
  alternative code.
- **5.5 GST invoice on personal account: explain post-purchase
  impossibility (tax law), send invoice copy, walk them through business
  account setup for next time.**
- **5.6 Unrecognised charge: check subscriptions/family orders first**,
  then genuine-unknown → fraud path (card-block advice, dispute, human
  security review).
- **5.7 Expired wallet credit: one-time re-credit for service credits
  (goodwill/refund credits) expired <30 days and unused; promotional
  credits stay expired**, explained kindly with the expiry date shown.

## Section 6 — Quality, Warranty & Installation
- **6.1 Fails after window, within warranty: route to brand + stay
  involved** — service-centre contacts + invoice; if brand unresponsive
  after ONE documented customer attempt → human intervenes with the brand.
- **6.2 Installation not scheduled: priority re-book + proactive check** —
  agent also proactively checks installation status whenever an
  installable item comes up in any chat.
- **6.3 Missing freebie: investigate packing records first** ✏️ — verify
  weight/packing logs (consistent with 1.5), then ship freebie or credit
  its fair value, customer's choice; flag listing if seller
  misrepresentation. (Default skipped the investigation gate.)
