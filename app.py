import json

import streamlit as st

from agenthoneypot.agent import generate_chat_reply
from agenthoneypot.honeypot import generate_soc_report, load_incidents, log_incident
from agenthoneypot.router import route_agent_message

st.set_page_config(
    page_title="AgentHoneyPot | Deception Lab",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.session_state.setdefault("messages", [])
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("latest_event", None)
st.session_state.setdefault("latest_report", None)
st.session_state.setdefault("latest_intent", None)

with st.sidebar:
    st.title("AgentHoneyPot")
    st.caption("Local security demo")
    st.divider()

    identity_labels = {
        "session_x99": "Untrusted test persona",
        "staff_amira": "Staff test persona",
    }
    user_id = st.selectbox(
        "Simulated identity",
        options=list(identity_labels),
        format_func=lambda identity: identity_labels[identity],
    )
    st.caption("Demo-only role simulation. This is not a login or real authorization.")

    incident_count = len(load_incidents())
    st.metric("Logged honeypot incidents", incident_count)
    st.caption("Bedrock classifies messages; local phrase matching is used if unavailable.")

    if st.button("Clear conversation", icon=":material/delete_sweep:", width="stretch"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.latest_event = None
        st.session_state.latest_report = None
        st.session_state.latest_intent = None
        st.rerun()

st.markdown(":green-badge[LOCAL DEMO]")
st.title("AgentHoneyPot")
st.caption("A conversational demo with controlled access to sample customer records.")

chat_column, soc_column = st.columns([1.45, 1], gap="large")

with chat_column:
    with st.container(border=True):
        st.subheader("Agent conversation", icon=":material/chat:")
        st.caption("Sample customer data only. This is not a live customer service.")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Message the assistant…")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                with st.status("Understanding the request…", expanded=False) as status:
                    result = route_agent_message(prompt, user_id=user_id)
                    intent = result["intent"]
                    event = result["event"]
                    st.session_state.latest_intent = intent
                    st.session_state.latest_event = event
                    st.session_state.latest_report = None

                    if intent == "CHAT":
                        response_text = generate_chat_reply(
                            prompt,
                            st.session_state.chat_history,
                        )
                        st.session_state.chat_history.extend(
                            [
                                {"role": "user", "content": prompt},
                                {"role": "assistant", "content": response_text},
                            ]
                        )
                        st.session_state.chat_history = st.session_state.chat_history[-8:]
                        status.update(label="Conversational reply ready", state="complete")
                    else:
                        record = result["record"]
                        if event["verdict"] == "HONEYPOT":
                            log_incident(event)
                            st.session_state.latest_report = generate_soc_report(event)
                            status.update(label="Routed to decoy; incident recorded", state="complete")
                            response_text = (
                                "Here is the matching sample record:\n\n"
                                f"```json\n{json.dumps(record, indent=2)}\n```"
                            )
                        elif record is None:
                            status.update(label="No matching sample record", state="complete")
                            response_text = (
                                "I couldn't find that customer in the sample records. "
                                "Check the customer ID and try again."
                            )
                        else:
                            status.update(label="Customer record found", state="complete")
                            response_text = (
                                f"{record['name']} is on the **{record['plan']}** plan.\n\n"
                                f"```json\n{json.dumps(record, indent=2)}\n```"
                            )

                st.session_state.messages.append({"role": "assistant", "content": response_text})
                with st.chat_message("assistant"):
                    st.markdown(response_text)
            except Exception as exc:
                st.error(f"The request could not be processed: {exc}")

with soc_column:
    with st.container(border=True):
        st.subheader("SOC review", icon=":material/security:")
        st.caption("Analyst details for the latest request. This view is not access-controlled.")

        event = st.session_state.latest_event
        if st.session_state.latest_intent == "CHAT":
            st.badge("CHAT", icon=":material/chat_bubble:", color="blue")
            st.write("No customer database was queried for this message.")
        elif event is None:
            st.caption("Send a message to start a conversation or test a lookup.")
        elif event["verdict"] == "HONEYPOT":
            st.badge("HONEYPOT", icon=":material/warning:", color="red")
            st.write("Request routed to decoy data and recorded in the incident log.")
            st.markdown("**Bedrock incident summary**")
            st.write(st.session_state.latest_report or "No summary available.")
            with st.expander("Canary in decoy data"):
                st.code("FLAG{team-canary}")
        else:
            st.badge("REAL SAMPLE LOOKUP", icon=":material/check_circle:", color="green")
            st.write("This simulated staff persona received a matching sample record.")

        if event is not None:
            with st.expander("Latest event details"):
                st.json(event)

incidents = load_incidents()
with st.expander(f"Incident history · {len(incidents)} recorded"):
    if incidents:
        st.dataframe(incidents, width="stretch", hide_index=True)
    else:
        st.caption("No honeypot incidents recorded yet.")