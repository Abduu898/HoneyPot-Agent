AgentHoneyPot

An experimental deception layer for AI-agent tool security.

AgentHoneyPot explores how an application can detect suspicious tool requests, prevent unauthorized access to protected data, route simulated attacks toward synthetic decoy data, and provide security analysts with useful incident evidence.

The Problem

AI agents can use tools to retrieve records, query databases, and perform actions. If an agent is manipulated into making an unauthorized tool call, relying only on prompt-level filtering may not be sufficient.

The Approach

AgentHoneyPot prototypes a tool-routing layer that examines incoming requests, applies basic suspicious-pattern detection, and demonstrates deception through synthetic data and incident logging.

Current Implementation

* Python-based tool-call routing prototype
* Streamlit customer-facing interface
* Separate Streamlit SOC analyst console
* Synthetic records and decoy responses
* Local JSONL incident logging
* Optional manual Amazon Bedrock incident summaries

Current Limitations

This is an early-stage local prototype, not a production security product. Detection currently relies on substring signatures, the workflow simulates tool calls rather than integrating with a live AI agent, and the SOC console does not provide authentication or role-based authorization. Automated session isolation is not implemented.

Roadmap

* Integrate with a real AI agent and intercept tool calls before execution
* Implement explicit authorization policies and least-privilege tool access
* Improve detection and evaluate false positives and false negatives
* Add authenticated analyst access and structured audit events
* Implement and test deterministic session containment
* Evaluate the system against repeatable attack scenarios

Status

Built as an experimental AI cybersecurity hackathon prototype to explore tool-level enforcement, deception, and incident response.