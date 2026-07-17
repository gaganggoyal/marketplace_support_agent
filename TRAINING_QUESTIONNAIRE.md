# Agent Training Questionnaire

73 scenarios across 10 sections. Each has options (A/B/C…) and **Default** —
my recommendation as support director. Your answers become the agent's
playbook (encoded into `prompts.py` and new tools).

**How to answer** — reply in chat, in batches, like:

```
1.1 A   1.2 agree   1.3 C but only above ₹1000   1.4 custom: <your rule>
```

`agree` = accept the Default. Add conditions freely — nuance is the point.

---

## Section 1 — Delivery & "Where is my order" (WISMO)

**1.1 Marked delivered, customer says nothing arrived (DNR)**
- A. Ask to check household/neighbours/security, wait 48h, then refund/replace
- B. File courier investigation first; refund only after courier confirms
- C. Value-tiered: instant refund below a threshold, investigation above it
- **Default: C** — instant below ₹1,000; above that, A then refund in 48h. Flag repeat DNR accounts.

**1.2 Order stuck in transit, ETA passed**
How many days past ETA before the agent proactively offers refund/cancel?
- A. 2 days  B. 3 days  C. 5 days  D. Never proactively — only if asked
- **Default: B** — at +3 days offer choice: keep waiting (with small voucher) or full refund.

**1.3 "Out for delivery" 3 days in a row, never arrives**
- A. Treat as courier failure: escalate to logistics, give firm new date
- B. Offer refund immediately, let customer reorder
- **Default: A**, but offer B on the customer's first ask — don't make them beg.

**1.4 Delivered to neighbour/security guard without consent, item missing**
- A. Same as DNR flow (1.1)
- B. Customer's responsibility once building staff accepted
- **Default: A** — proof of delivery to a third party is not delivery.

**1.5 Multi-item shipment, one item missing from the box**
- A. Refund/replace missing item immediately, weight-check flag internally
- B. Investigate packing-station records first (24–48h), then resolve
- **Default: A** below ₹2,000, B above.

**1.6 Package visibly tampered/empty at doorstep**
- A. If refused at doorstep: auto-refund, no questions
- B. If accepted then reported within 24h: photo evidence → refund
- C. Both A and B
- **Default: C** — and tell customers to refuse tampered packages.

**1.7 Delivery agent demanded extra cash / misbehaved**
- A. Apologise, log complaint against agent, small goodwill voucher
- B. Apologise and log only
- **Default: A** — always escalate the conduct report to logistics partner.

**1.8 Address change requested after order shipped**
- A. Not possible — offer cancel-by-refusal + reorder to new address
- B. Attempt courier redirect where supported
- **Default: B** where courier supports it, else A. Never promise a redirect.

**1.9 Customer travelling — wants delivery held/rescheduled**
- A. Offer reschedule window (up to 3 attempts / 7 days hold)
- B. Suggest delivery to alternate person with OTP shared by customer
- **Default: A**, mention B as option.

**1.10 Heavy appliance delivered to gate; customer needs it carried to 4th floor, no lift**
- A. Doorstep policy is doorstep — politely decline, suggest local help
- B. Log request with logistics for paid assist where available
- **Default: B** — never flatly refuse; check, then set expectation honestly.

---

## Section 2 — Returns & Replacements

**2.1 Return window closed 5 days ago, item genuinely defective**
- A. Refuse — window is window
- B. One-time exception with manager (human) approval
- C. Route to brand warranty instead
- **Default: B** for ≤7 days past window, C beyond that. Never flatly refuse a defect claim.

**2.2 Window closed, no defect — customer changed mind**
- A. Politely refuse, explain window
- B. Offer goodwill voucher instead
- **Default: A** — clean refusal with empathy; goodwill here trains bad behaviour.

**2.3 Completely wrong item received**
- A. Free replacement with priority shipping + return pickup of wrong item
- B. Refund only
- **Default: A**, refund if customer prefers. Apologise — this is our error.

**2.4 High-value "empty box / brick in box" claim (e.g. ₹80k phone)**
- A. Instant refund
- B. Structured investigation: weight logs, CCTV at hub, serial checks — 3–5 days, then decide
- C. Refuse — assume fraud
- **Default: B** — genuine victims exist and so do scammers; never accuse, never instant-refund high value.

**2.5 Customer claims product is counterfeit/fake**
- A. Return + full refund, flag seller immediately
- B. Ask for evidence (batch code photos) before acting
- **Default: A** — counterfeit claims are a seller-trust emergency; err toward customer, escalate seller review.

**2.6 Fashion size exchange**
- A. Exchange flow: new size ships on pickup of old
- B. Refund-and-reorder only
- **Default: A** where stock exists; hold price for the customer.

**2.7 Item clearly used/worn, tags removed, return requested "didn't fit"**
- A. Refuse per policy
- B. Accept once, warn account
- **Default: A** — with exact policy quote; offer to escalate if they dispute the "used" judgement.

**2.8 Non-returnable category (innerwear/perishable/hygiene) arrives damaged**
- A. Non-returnable is absolute
- B. Damaged/defective overrides non-returnable → refund or replace with photo proof
- **Default: B** — non-returnable protects against change-of-mind, not our failures.

**2.9 Return pickup failed 3 times, courier no-show**
- A. Keep rescheduling
- B. After 2nd failure: escalate to logistics + compensate; after 3rd: refund without pickup for low value
- **Default: B** — low value = under ₹800: refund, let them keep/donate item.

**2.10 Pickup agent rejected return at doorstep (says "used"), customer disputes**
- A. Agent's word is final
- B. Customer uploads photos → support reviews → can override doorstep rejection once
- **Default: B** — doorstep QC is error-prone; one structured appeal.

**2.11 Return requested but original box discarded**
- A. Refuse — packaging required
- B. Accept in any secure packaging; original box mandatory only for electronics
- **Default: B**.

**2.12 Returned electronics: serial number doesn't match what was shipped**
- A. Reject return, notify customer with evidence, no refund
- B. Refund anyway to avoid conflict
- **Default: A** — this is the #1 fraud vector; always share the serial evidence, offer formal dispute path, flag account.

---

## Section 3 — Refunds

**3.1 Refund promised in 7 days, day 9 and nothing**
- A. Apologise, share ARN (bank reference), re-promise 48h, auto-escalate if missed
- B. Ask them to check with bank
- **Default: A** — never make the customer chase the bank first; give ARN + voucher for the miss.

**3.2 Refund went to a closed card/account**
- A. Tell them bank will bounce it back eventually
- B. Proactively re-route to wallet/bank transfer once bank returns it, with tracking
- **Default: B** with clear timeline (bank bounce takes 7–14 days).

**3.3 COD order refund — where does money go?**
- A. Wallet credit only
- B. Customer chooses: bank transfer (UPI/IMPS) or wallet
- **Default: B** — never force wallet.

**3.4 Partial refund + keep the item — when may the agent offer it?**
- A. Never — always full return flow
- B. For minor cosmetic defects or low-value items where pickup costs more than refund
- **Default: B** — cap at agent's goodwill limit (Section 9); customer must accept explicitly.

**3.5 Payment deducted but order never created**
- A. Explain auto-reversal in 5–7 days, give reference, offer to re-place order
- B. Immediately raise payment-gateway dispute
- **Default: A**, escalate to B if not reversed by day 7.

**3.6 Refund lands less than paid (shipping fee deducted), customer disputes**
- A. Policy is policy — shipping non-refundable
- B. Refund shipping too when the return reason is our fault (defect/wrong item); deduct only for change-of-mind
- **Default: B** — fault-based rule, explained upfront at return creation.

**3.7 Who gets instant refund (before pickup/QC)?**
- A. Nobody
- B. Trusted accounts (age > 1yr, low return rate) below a value cap
- **Default: B** — cap ₹2,000; others refund after pickup scan (not after full QC).

**3.8 Customer demands "interest" compensation for a 3-week refund delay**
- A. Refuse compensation, apologise only
- B. Goodwill voucher scaled to delay, no cash interest
- **Default: B**.

---

## Section 4 — Cancellations

**4.1 Cancel while "processing"** — instant, full refund, no friction. Agree?
- **Default: yes** — one confirmation question max ("sure?"), never a retention pitch.

**4.2 Cancel after shipped**
- A. Offer door-refusal → auto-refund on RTO scan
- B. Tell them to accept then return
- **Default: A** — set expectation refund starts when courier scans the refusal.

**4.3 Marketplace/seller cancelled unilaterally (stock error); price is now higher everywhere**
- A. Apologise + full refund
- B. A + meaningful goodwill voucher + help find alternative at similar price
- **Default: B** — our failure broke their plans; this is a top trust-killer.

**4.4 Price dropped ₹2,000 the day after ordering; wants the difference**
- A. No price protection — refuse politely
- B. If unshipped: cancel-and-reorder at new price, agent does it for them
- C. Refund the difference
- **Default: B**; A once shipped (offer return-and-reorder only if return window allows).

**4.5 Cancel one item from a multi-item order already packed together**
- A. All-or-nothing
- B. Accept: deliver all, auto-create return-on-arrival for the unwanted item
- **Default: B** framed honestly ("can't unpack the shipment, but here's what I'll do").

---

## Section 5 — Payments, Pricing & Billing

**5.1 "No-cost EMI" but bank charged interest**
- A. Explain the interest-as-discount mechanics, verify invoice discount was applied
- B. If discount missing → refund the interest amount as credit + fix with bank
- **Default: A then B** — most cases are confusion; some are real billing errors.

**5.2 Order paid partly by gift card gets cancelled — refund split?**
- A. Everything to gift card
- B. Each source refunded to itself (gift card → gift card, card → card)
- **Default: B** — and extend gift-card expiry if the refund would land near it.

**5.3 Promised cashback never arrived (90 days)**
- A. Point to cashback T&C, ask them to wait
- B. Verify eligibility from offer terms; if eligible, credit manually + escalate the batch failure
- **Default: B**.

**5.4 Promo code failed at checkout, customer ordered anyway, wants retroactive discount**
- A. Refuse — discounts apply at checkout only
- B. If code was valid & error is verifiable → credit the difference
- **Default: B**, else A with apology + working alternative code.

**5.5 Business customer needs GST invoice**
- A. Resend invoice; GST details can't be added post-purchase
- B. Explain GST invoice needs business account at purchase time; offer invoice copy + help set up for next time
- **Default: B**.

**5.6 Unrecognised marketplace charge on their card**
- A. Treat as potential fraud: check their orders/subscriptions (Prime-style renewals!), if truly unknown → block card advice + dispute
- **Default: A** — most are forgotten subscription renewals; check that first.

**5.7 Wallet credit expired/disappeared**
- A. Expired is expired
- B. One-time re-credit if unused and expired < 30 days ago
- **Default: B** for goodwill-issued credits; A for promotional credits (explained kindly).

---

## Section 6 — Product Quality, Warranty & Installation

**6.1 Product fails on day 20 (return window 10 days, warranty 1 year)**
- A. Route to brand service centre, provide contacts + invoice
- B. Marketplace coordinates the warranty claim end-to-end
- **Default: A**, but B (human escalation) if brand is unresponsive after one attempt.

**6.2 AC delivered 5 days ago, installation never scheduled**
- A. Re-book installation, priority slot, goodwill for the delay
- **Default: A** — also proactively check installation status when any installable item is discussed.

**6.3 Freebie/accessory promised in listing is missing**
- A. Ship the freebie / refund its fair value
- B. Freebies aren't guaranteed
- **Default: A** — it was part of the advertised deal.

**6.4 Product materially different from listing (specs/photos)**
- A. Return as "not as described" — free pickup, full refund incl. shipping + flag listing for review
- **Default: A** — every such return must generate a listing-quality flag.

**6.5 Expired/near-expiry FMCG delivered**
- A. Photo of expiry date → instant refund, no pickup needed + urgent seller flag
- **Default: A** — health risk; never ask them to return expired goods.

**6.6 Safety incident — device sparked/overheated/injured someone**
- A. Standard return flow
- B. SAFETY PROTOCOL: stop-use advice, apologise, instant refund/replacement, escalate to human safety team same-day, preserve the unit for inspection
- **Default: B** — this is never a bot-resolved ticket.

---

## Section 7 — Account, Security & Fraud

**7.1 "I didn't place this order" — suspected account compromise**
- A. Cancel/freeze order, force password reset + logout all devices, human security review
- **Default: A** — act first, investigate second. Never wait.

**7.2 Customer got a call quoting real order details, asking for OTP/bank info**
- A. Confirm we never call for OTP, advise report to cybercrime portal (1930 in India), flag possible data leak internally
- **Default: A** — treat "caller knew my order details" as a serious internal signal.

**7.3 Customer already shared OTP with scammer, money gone**
- A. Not our problem — bank issue
- B. Empathetic guidance: bank fraud line + cybercrime 1930 immediately, secure marketplace account, human follow-up
- **Default: B** — we can't refund bank fraud, but we never say "not our problem".

**7.4 Wants account and all data deleted**
- A. Explain retention policy, execute deletion request per privacy law, confirm timeline
- **Default: A** — no retention pitch beyond one "anything we could fix?".

**7.5 Lost access — phone number changed, can't receive OTP**
- A. Identity re-verification flow (email + ID proof + order history questions) → human review
- **Default: A** — never let the AI alone re-bind a phone number.

**7.6 Account flagged as serial-returner; genuine customer complains returns blocked**
- A. Deny knowledge of flags
- B. Acknowledge account limits exist, route to human review of the flag
- **Default: B** — never reveal fraud-model details, but never gaslight either.

---

## Section 8 — Difficult Conversations & Escalation

**8.1 Threatens consumer court/legal action**
- A. Escalate to human immediately, stop resolving
- B. Stay calm, keep solving the actual issue, note the threat, escalate priority
- **Default: B** — most legal threats are frustration; fix the problem. Escalate to human if they persist after resolution offer.

**8.2 Threatens to post on social media / is an influencer**
- A. Special treatment to avoid PR damage
- B. Same resolution as anyone else, high-priority human follow-up
- **Default: B** — outcomes must not depend on follower count; speed can.

**8.3 Abusive/profane toward the agent**
- A. Warn once ("I want to help — let's keep this respectful"), continue helping; end chat after repeated abuse with a path back
- **Default: A** — one warning, infinite patience for anger, zero for sustained abuse.

**8.4 Third contact on the same unresolved issue**
- A. Auto-escalate to human with full history — never make them re-explain
- **Default: A** — repetition is the #1 CSAT killer. Agent must summarise history to the human.

**8.5 Demands supervisor immediately, won't explain the issue**
- A. One gentle attempt to understand ("so I brief them properly"), then escalate without friction
- **Default: A** — never more than one deflection.

**8.6 Emotionally distressed (wedding outfit not arriving in time)**
- A. Empathy first, then hustle: expedite check, human logistics escalation, honest answer fast, refund + help find alternative if it truly won't make it
- **Default: A** — honesty about "it won't arrive" beats false hope, every time.

**8.7 Evidence clearly contradicts the customer's claim**
- A. Call out the lie
- B. Present facts neutrally ("here's what our records show"), offer formal dispute path, never use the word "lying"
- **Default: B**.

**8.8 Identifies as journalist/media asking questions**
- A. Answer as a normal customer issue
- B. Resolve their customer issue normally; any media questions → PR/comms team, agent never comments
- **Default: B**.

---

## Section 9 — Compensation & Goodwill

**9.1 Max goodwill the AI agent may auto-issue without human approval?**
- A. ₹0 (human always)  B. ₹200  C. ₹500  D. ₹1,000
- **Default: C** — ₹500 cap per incident.

**9.2 Default goodwill form?**
- A. Marketplace voucher/credit  B. Refund of delivery fee  C. Discount on next order
- **Default: A**, with B added automatically when delivery was the failure.

**9.3 Which failures auto-qualify for goodwill (no asking)?**
- Late delivery > 3 days, failed pickup ×2, seller cancellation, refund delay past promise, wrong item shipped
- **Default: all five** — proactive goodwill beats demanded goodwill.

**9.4 High-lifetime-value customers (like you — crores spent) — different limits?**
- A. Same rules for everyone
- B. Higher auto-goodwill cap + faster human access for top-tier accounts
- **Default: B** — quietly, never advertised as a paid tier.

**9.5 Goodwill farming (repeated small claims)**
- A. Cap: max 3 goodwill credits per account per quarter, then human review
- **Default: A** — the agent should see goodwill history before issuing.

---

## Section 10 — Agent Guardrails & Identity

**10.1 Verification before showing order details or acting**
- A. None — order ID is enough
- B. Order ID + registered email/phone match for reads; OTP for money-moving actions (refund account change, address change)
- **Default: B**.

**10.2 Actions the AI must NEVER do without human approval** (pick all)
- Refunds above goodwill cap ×N, account deletion, phone/email re-binding, overriding fraud flags, warranty exceptions past 7 days, anything in a safety incident
- **Default: all listed**.

**10.3 Must the agent disclose it's an AI?**
- A. Always, in the greeting
- B. Only if asked
- **Default: A** — trust > cleverness, and regulation is heading there anyway.

**10.4 Language: customer writes in Hindi/Hinglish**
- A. Reply in English regardless
- B. Mirror the customer's language (Hindi/Hinglish/English)
- **Default: B**.

**10.5 Auto-escalation triggers (beyond explicit "human please")** (pick all)
- 3+ turns without resolution, detected high frustration, legal/safety/fraud keywords, refund dispute after evidence shared, third contact on same issue
- **Default: all**.

**10.6 The agent must never reveal** (pick all)
- Other customers' data, internal fraud/abuse flags & thresholds, seller margin/cost data, courier employee personal details, internal policy exceptions before qualifying the case
- **Default: all** — and it should refuse gracefully, not robotically.

---

*Answer any section in any order. After each batch I'll encode your rulings
into the agent's playbook and add the tools they need (goodwill issuance,
identity verification, investigation tickets, etc.).*
