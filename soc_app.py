"""Standalone Streamlit entry point for SOC incident review."""

import streamlit as st

st.set_page_config(
    page_title="FastFood Corp | SOC console",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from agenthoneypot.honeypot import generate_soc_report, load_incidents

st.title("Security operations", icon=":material/shield:")
st.caption("Honeypot events, query-signature verdicts, and analyst summaries.")
st.warning(
    "Demo only: this separate app is not protected by authentication or role-based access control. "
    "Keep it on a trusted environment until identity controls are configured."
)

incidents = list(reversed(load_incidents()))
unique_sessions = {event.get("user_id", "unknown") for event in incidents}

incident_metric, session_metric, detector_metric = st.columns(3, wrap=True)
incident_metric.metric("Honeypot incidents", len(incidents))
session_metric.metric("Flagged sessions", len(unique_sessions))
detector_metric.metric("Detection method", "Query signatures")

st.subheader("Incident review", icon=":material/troubleshoot:")

if incidents:
    def incident_label(index: int) -> str:
        incident = incidents[index]
        timestamp = incident.get("timestamp", "Unknown time")
        user_id = incident.get("user_id", "unknown")
        query = incident.get("query", "").replace("\n", " ")
        return f"{timestamp} | {user_id} | {query[:72]}"

    selected_index = st.selectbox(
        "Select an incident",
        options=range(len(incidents)),
        format_func=incident_label,
        key="soc_selected_incident",
    )
    selected_incident = incidents[selected_index]
    report_key = selected_incident.get("timestamp", incident_label(selected_index))
    reports = st.session_state.setdefault("soc_report_cache", {})

    summary_column, details_column = st.columns([1.4, 1], gap="large", wrap=True)
    with summary_column:
        with st.container(border=True):
            st.markdown("#### Analyst summary")
            if st.button(
                "Generate Bedrock summary",
                type="primary",
                icon=":material/auto_awesome:",
                width="stretch",
            ):
                with st.spinner("Generating incident summary..."):
                    reports[report_key] = generate_soc_report(selected_incident)
            if report_key in reports:
                st.write(reports[report_key])
            else:
                st.caption("Generate a summary when an analyst is ready to review this event.")

    with details_column:
        with st.container(border=True):
            st.markdown("#### Event details")
            st.json(selected_incident)

    st.subheader("Audit trail", icon=":material/table_view:")
    st.dataframe(incidents, hide_index=True, width="stretch")
else:
    st.info("No honeypot incidents yet. Submit a test request from the customer portal.")