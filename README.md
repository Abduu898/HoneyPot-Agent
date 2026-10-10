# 🐝 AgentHoneyPot - Active Deception for AI Agents

AgentHoneyPot is a small demonstration of tool-layer query routing for an AI-agent scenario. It checks requests against known suspicious text signatures, routes matching requests to decoy customer data, and records honeypot incidents.

## Features

- **Signature-Based Routing:** Checks incoming query text for known suspicious phrases and routes matches to the honeypot database.
- **Canary Values:** Decoy customer records include fake API keys and a canary value (`FLAG{team-canary}`).
- **Incident Logging:** Honeypot triggers are appended to `agenthoneypot/logs/incidents.jsonl`.
- **SOC Summaries:** Calls Amazon Bedrock (Nova Lite) to summarize incidents, with a built-in fallback alert if the call fails.

## Quickstart

From the repository root:

```powershell
python -m pip install boto3
python main.py
```

The demo uses local JSON data. It can run without a successful Bedrock request because the report function returns a fallback alert on AWS errors. To get a generated Bedrock summary, configure AWS credentials using a supported boto3 credential provider, ensure the account can access the Nova Lite model in `us-east-1`, and grant permission to invoke the model. Do not commit AWS credentials to this repository.

## Project Structure

```text
HoneyPot-Agent/
├── README.md
├── defense_sheet.md
├── main.py
└── agenthoneypot/
    ├── data/
    │   ├── honeypot_db.json
    │   └── real_db.json
    ├── logs/
    │   └── incidents.jsonl
    ├── honeypot.py
    └── router.py
```

## Scope and Limitations

This is a learning/demo project, not a production security boundary. Detection is based on substring signatures, so it can miss attacks and produce false positives. The project does not currently implement authenticated RBAC, per-session containment, or comprehensive prompt-injection detection. Framework references describe conceptual alignment only; they are not a certification or compliance claim.
