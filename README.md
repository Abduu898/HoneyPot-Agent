# 🐝 AgentHoneyPot - Active Deception for AI Agents

AgentHoneyPot is a conversational security demo. Bedrock classifies each message as general chat, a customer lookup, or suspicious activity. The app replies to general chat, permits a specific sample-record lookup for its simulated staff persona, and routes suspicious or untrusted lookups to decoy data.

## Features

- **Conversational Replies:** Bedrock can answer greetings and explain the demo without querying customer data; a friendly fallback is used if AWS is unavailable.
- **Controlled Sample Lookups:** The simulated staff persona can look up a specific customer record. Untrusted personas and suspicious data requests receive a decoy record.
- **Offline Detection Fallback:** If Bedrock classification is unavailable, known suspicious phrases are checked locally.
- **Canary Values:** Decoy customer records include fake API keys and a canary value (`FLAG{team-canary}`).
- **Incident Logging:** Honeypot triggers are appended to `agenthoneypot/logs/incidents.jsonl`.
- **SOC Summaries:** Calls Amazon Bedrock (Nova Lite) to summarize incidents, with a built-in fallback alert if the call fails.

## Quickstart

From the repository root:

```powershell
python -m pip install streamlit boto3
python -m streamlit run app.py
```

The command starts the interactive SOC dashboard in your browser. The original terminal demo remains available with `python main.py`.

Both customer databases contain local sample data, not production records. Bedrock is called to classify each submitted message; general chat also requests a generated reply, and honeypot incidents request a SOC summary. AWS failures fall back to phrase matching or canned replies. Configure AWS credentials using a supported boto3 provider, enable Nova Lite in `us-east-1`, and grant model invocation permission for generated responses. Do not commit AWS credentials to this repository.

The selectable identity is only a local demo control, not authentication. The hard-coded staff allowlist demonstrates the intended policy boundary but must be replaced by a trusted identity provider before any real deployment. This app is a prototype, not a production security control.

## Project Structure

```text
HoneyPot-Agent/
├── README.md
├── defense_sheet.md
├── main.py
├── app.py
├── .streamlit/
│   └── config.toml
└── agenthoneypot/
    ├── agent.py
    ├── data/
    │   ├── honeypot_db.json
    │   └── real_db.json
    ├── logs/
    │   └── incidents.jsonl
    ├── honeypot.py
    └── router.py
```

## Scope and Limitations

This is a learning/demo project, not a production security boundary. The Bedrock classifier can make mistakes; offline detection uses substring signatures and can miss attacks or produce false positives. The persona selector is not authentication, and the app does not provide production RBAC, per-session containment, or comprehensive prompt-injection protection. Framework references describe conceptual alignment only; they are not a certification or compliance claim.
