# Defense sheet: AgentHoneyPot

## 1. Threat scenario

A user submits a prompt-injection or data-exfiltration request through an order note or support message, attempting to access records or privileged values.

## 2. Demo architecture

- **Signature-based detection:** The router checks request text against a fixed list of suspicious phrases. It can miss novel wording and may flag benign requests.
- **Decoy routing:** A matching request receives data from `honeypot_db.json`; other requests receive data from `real_db.json`.
- **Separate interfaces:** The customer portal (`app.py`) and SOC console (`soc_app.py`) run as separate Streamlit applications. The customer portal does not display the internal verdict, event record, or Bedrock summary.
- **Incident log:** Honeypot events are appended to `agenthoneypot/logs/incidents.jsonl` for analyst review.

The current sample decoy contains a manager-override canary value and a canary endpoint. Treat these as demo indicators, not real credentials or a real endpoint.

## 3. Security mapping

- **NIST CSF 2.0 concepts:** The demo illustrates **Detect** through signature matches and incident records, and **Respond** through decoy routing. This is conceptual alignment, not certification or compliance.
- **OWASP agentic risks:** The demo illustrates risks associated with excessive agency and privilege escalation. It does not replace authorization or fully mitigate these risks.

## 4. SOC workflow and limitations

An analyst can select a logged incident in the SOC console and request a concise Amazon Bedrock Nova Lite summary. The request requires AWS credentials, model access, and permission to invoke Bedrock in `us-east-1`; a local fallback alert is returned if the call fails.

The customer and SOC apps run as separate processes, but this is not by itself an authorization boundary. The SOC app is currently accessible without authentication. The demo also does not implement per-session containment, a real payment/order backend, or comprehensive prompt-injection detection. Configure an identity provider and enforce analyst roles before deployment.
