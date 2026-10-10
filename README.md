# AgentHoneyPot | Active Deception Demo

A Streamlit honeypot demonstration with separate customer-facing and analyst applications. Suspicious tool requests are routed to decoy data, while analysts can review the recorded events.

## Run locally

Install dependencies from the repository root:

```powershell
python -m pip install streamlit boto3
```

Start the customer portal in one terminal:

```powershell
python -m streamlit run app.py --server.port 8501
```

Start the SOC console in another terminal, bound to your computer only:

```powershell
python -m streamlit run soc_app.py --server.port 8503 --server.address 127.0.0.1
```

The customer portal opens at `http://localhost:8501`; the SOC console opens at `http://127.0.0.1:8503`. They are separate Streamlit entry points and processes. The SOC console is intentionally kept local because it does not have authentication or role-based authorization.

Use the SOC console's **Tool-call simulation** to submit a benign or suspicious tool query and inspect the exact JSON payload returned to a simulated caller. Signature matches receive realistic synthetic decoy data and are recorded in `agenthoneypot/logs/incidents.jsonl`; the customer portal continues to show ordinary confirmations. This is a local honeypot simulation, not a live AI-agent integration.

Analysts can manually request an Amazon Bedrock Nova Lite summary in `us-east-1`; the simulator itself does not call Bedrock. A fallback alert is returned if the summary request fails.

Configure AWS credentials through a supported boto3 provider and grant Bedrock model access to receive generated summaries. Never put AWS credentials in the repository.

## Project structure

```text
HoneyPot-Agent/
├── .streamlit/
│   └── config.toml
├── app.py
├── soc_app.py
├── agenthoneypot/
│   ├── data/
│   │   ├── honeypot_db.json
│   │   └── real_db.json
│   ├── logs/
│   │   └── incidents.jsonl
│   ├── honeypot.py
│   └── router.py
├── defense_sheet.md
└── main.py
```

## Important limitations

This is a local demo, not a production security boundary. Detection uses substring signatures. The SOC app runs separately from the customer portal but does not currently authenticate users or enforce roles. The customer workflow does not process real transactions or persist real orders. Add an identity provider and enforce analyst roles at the deployment boundary before exposing the SOC app to a network.
