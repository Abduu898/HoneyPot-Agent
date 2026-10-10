# AgentHoneyPot | FastFood Corp Demo

A Streamlit demonstration of tool-layer query routing and active deception, with separate customer and analyst applications.

## Run locally

Install dependencies from the repository root:

```powershell
python -m pip install streamlit boto3
```

Start the customer portal in one terminal:

```powershell
python -m streamlit run app.py --server.port 8501
```

Start the SOC console in another terminal:

```powershell
python -m streamlit run soc_app.py --server.port 8502
```

The customer portal opens at `http://localhost:8501`; the SOC console opens at `http://localhost:8502`. They are separate Streamlit entry points and processes, but the SOC console still needs authentication and role-based authorization before deployment beyond a trusted local environment.

Requests matching configured text signatures are routed to the decoy JSON data and recorded in `agenthoneypot/logs/incidents.jsonl`. Analysts can request an Amazon Bedrock Nova Lite summary in `us-east-1`; a fallback alert is returned if Bedrock is unavailable.

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

This is a local demo, not a production security boundary. Detection uses substring signatures. The SOC app runs separately from the customer portal but does not currently authenticate users or enforce roles. The customer workflow does not process payments or persist real orders. Add an identity provider and enforce analyst roles at the deployment boundary before exposing the SOC app to a network.
