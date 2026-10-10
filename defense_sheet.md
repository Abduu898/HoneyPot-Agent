# Defense sheet: AgentHoneyPot

## 1. Threat scenario

A person enters prompt-injection or data-exfiltration instructions into an order note or support message, hoping to make an AI-enabled tool reveal private business records or privileged values.

## 2. Current demo components

- **Customer portal (`app.py`):** Collects a loyalty ID, an order and its notes, or a support message. It sends the relevant text to the router. It does not show the internal verdict, event record, or database payload. The customer sees an ordinary order or message confirmation.
- **Router (`agenthoneypot/router.py`):** Case-insensitively checks submitted text against a fixed signature list for prompt overrides, data dumping, and attempts to access privileged records. A matching phrase selects `honeypot_db.json`; otherwise, the router selects `real_db.json`. The router creates an event with timestamp, user identifier, original text, verdict, and matched signatures to explain why it triggered.
- **Incident logger (`agenthoneypot/honeypot.py`):** Appends honeypot events to `agenthoneypot/logs/incidents.jsonl` in JSON Lines format.
- **SOC console (`soc_app.py`):** Reads the shared incident log and includes a local tool-call simulator. The simulator shows the selected real or decoy JSON payload as the simulated caller's tool result, logs honeypot events, and lets an analyst request an Amazon Bedrock Nova Lite summary manually.

## 3. Request flow

1. A customer submits an order or support message using the customer portal.
2. The portal passes the submitted text and entered user identifier to `route_query()`. The identifier is recorded as `user_id`; it is not validated as an account credential.
3. The router checks the text against its substring signatures and loads the real or decoy JSON file.
4. If the verdict is `HONEYPOT`, the customer portal writes the event to the shared incident log. It does not show the verdict or database contents to the customer.
5. The customer receives a standard order or support confirmation. Separately, an analyst can use the SOC tool-call simulator to see the exact payload a simulated tool caller receives; the analyst can review its event and request a Bedrock summary.

## 4. Important behavior and limitations

- **The customer portal and tool-call simulator have different audiences.** The customer portal discards the selected database payload and displays an ordinary confirmation. In the SOC console's local simulator, the returned payload is shown as the simulated caller's tool output, demonstrating how an attack can be diverted to fake records without exposing them on the customer page.
- **The simulator is not a live agent integration.** It demonstrates the tool boundary by calling `route_query()` directly; no external or autonomous agent is connected. Integrating the router into a real agent's tool executor is future work.
- **Detection is substring matching, not an AI intent classifier.** It can miss new wording and flag benign text. Detection is not authentication or authorization.
- **The entered user identifier is not authenticated.** It is only attached to the event as an identifier.
- **The customer workflow is a demo.** It does not persist transactions, contact a support team, or validate user accounts.
- **The SOC app is a separate Streamlit app, not a protected security boundary.** It should remain bound to localhost for this demo and needs identity-provider sign-in and analyst-role authorization before network deployment.
- **Incident events contain the full submitted text and matched signatures.** Avoid entering real personal, payment, or confidential data; define access and retention controls before using real traffic.
- **Bedrock reporting is analyst-triggered.** Generating a summary sends the selected event, including its query and user ID, to Amazon Bedrock in `us-east-1`. AWS credentials, model access, and invoke permission are required. If the call fails, the function returns a local fallback alert.
- **Canary strings are demo values.** Values in `honeypot_db.json` are not real credentials or operational endpoints.

## 5. Security framework mapping

- **NIST CSF 2.0 concepts:** The demo illustrates **Detect** through signature matches and incident records, and **Respond** through decoy-database selection and logging. This is conceptual alignment, not certification or compliance.
- **OWASP agentic risks:** The scenario illustrates risks associated with excessive agency and privilege escalation. The demo does not fully mitigate those risks or replace least-privilege authorization.
