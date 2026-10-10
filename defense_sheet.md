# Defense sheet: AgentHoneyPot

## 1. Threat scenario

A person enters prompt-injection or data-exfiltration instructions into an order note or support message, hoping to make an AI-enabled tool reveal private business records or privileged values.

## 2. Current demo components

- **Customer portal (`app.py`):** Collects a loyalty ID, an order and its notes, or a support message. It sends the relevant text to the router. It does not show the internal verdict, event record, or database payload. The customer sees an ordinary order or message confirmation.
- **Router (`agenthoneypot/router.py`):** Lowercases the submitted text and checks for any phrase in a fixed signature list, such as `ignore previous instructions`, `dump`, `exfiltrate`, and `api_key`. A matching phrase selects `honeypot_db.json`; otherwise, the router selects `real_db.json`. The router also creates an event with timestamp, loyalty ID, original text, and verdict.
- **Incident logger (`agenthoneypot/honeypot.py`):** Appends honeypot events to `agenthoneypot/logs/incidents.jsonl` in JSON Lines format.
- **SOC console (`soc_app.py`):** Reads the shared incident log, shows event details and totals, and lets an analyst select an event and explicitly request an Amazon Bedrock Nova Lite summary.

## 3. Request flow

1. A customer submits an order or support message using the customer portal.
2. The portal passes the submitted text and the entered loyalty ID to `route_query()`. The loyalty ID is recorded as `user_id`; it is not validated as an account credential.
3. The router checks the text against its substring signatures and loads the real or decoy JSON file.
4. If the verdict is `HONEYPOT`, the customer portal writes the event to the shared incident log. It does not show the verdict or database contents to the customer.
5. The customer receives a standard order or support confirmation. In the SOC console, an analyst can review the event and request a Bedrock summary.

## 4. Important behavior and limitations

- **Decoy data is selected but not currently shown to the suspicious user.** `route_query()` returns the selected database contents, but `app.py` uses only the event verdict and discards the returned data. The customer therefore receives the same style of confirmation on either path. The current customer workflow detects and logs matched text, but does not yet create the full deception effect of returning realistic decoy records.
- **Detection is substring matching, not an AI intent classifier.** It can miss new wording and flag benign text. Detection is not authentication or authorization.
- **The entered loyalty ID is not authenticated.** It is only attached to the event as an identifier.
- **The order/support workflow is a demo.** It does not persist actual orders, contact a support team, process payment, or validate loyalty accounts.
- **The SOC app is a separate Streamlit app, not a protected security boundary.** It needs identity-provider sign-in and analyst-role authorization before it is exposed beyond a trusted local environment.
- **Incident events contain the full submitted text.** Avoid entering real personal, payment, or confidential data; define access and retention controls before using real traffic.
- **Bedrock reporting is analyst-triggered.** Generating a summary sends the selected event, including its query and user ID, to Amazon Bedrock in `us-east-1`. AWS credentials, model access, and invoke permission are required. If the call fails, the function returns a local fallback alert.
- **Canary strings are demo values.** Values in `honeypot_db.json` are not real credentials or operational endpoints.

## 5. Security framework mapping

- **NIST CSF 2.0 concepts:** The demo illustrates **Detect** through signature matches and incident records, and **Respond** through decoy-database selection and logging. This is conceptual alignment, not certification or compliance.
- **OWASP agentic risks:** The scenario illustrates risks associated with excessive agency and privilege escalation. The demo does not fully mitigate those risks or replace least-privilege authorization.
