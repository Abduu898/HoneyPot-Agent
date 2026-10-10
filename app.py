import streamlit as st

st.set_page_config(
    page_title="FastFood Corp | Customer portal",
    page_icon="🍟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from agenthoneypot.honeypot import log_incident
from agenthoneypot.router import route_query

MENU = {
    "Double cheeseburger meal": "$12.50",
    "Crispy chicken sandwich": "$9.99",
    "Large fries and soda": "$5.50",
}


def process_customer_activity(query: str, loyalty_id: str) -> None:
    result = route_query(query, user_id=loyalty_id)
    event = result["event"]

    if event["verdict"] == "HONEYPOT":
        log_incident(event)


st.title("FastFood Corp", icon=":material/storefront:")
st.subheader("Order your favorites")
st.caption("Choose a meal or get help with an existing order. Demo checkout; no payment is collected.")

order_column, support_column = st.columns(2, gap="large", wrap=True)

with order_column:
    with st.container(border=True):
        st.subheader("Place an order", icon=":material/restaurant:")
        with st.form("customer_order_form"):
            loyalty_id = st.text_input("Loyalty ID", value="LF-40218")
            item = st.selectbox(
                "Menu item",
                list(MENU),
                format_func=lambda menu_item: f"{menu_item} ({MENU[menu_item]})",
            )
            quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
            notes = st.text_area(
                "Order notes",
                placeholder="Add preferences such as no pickles or extra sauce.",
                height=92,
            )
            order_submitted = st.form_submit_button(
                "Place order",
                type="primary",
                icon=":material/shopping_bag:",
                width="stretch",
            )

        if order_submitted:
            order_query = f"Order {item} x{quantity}. Customer notes: {notes}"
            with st.spinner("Submitting your order..."):
                process_customer_activity(order_query, loyalty_id)
            price = float(MENU[item].replace("$", ""))
            st.session_state["customer_confirmation"] = {
                "type": "order",
                "item": item,
                "quantity": quantity,
                "total": price * quantity,
            }

with support_column:
    with st.container(border=True):
        st.subheader("Contact support", icon=":material/support_agent:")
        with st.form("customer_support_form"):
            support_loyalty_id = st.text_input("Loyalty ID", value="LF-40218", key="support_loyalty_id")
            support_query = st.text_area(
                "How can we help?",
                placeholder="Describe an order, billing, or account issue.",
                height=160,
            )
            support_submitted = st.form_submit_button(
                "Send support request",
                icon=":material/send:",
                width="stretch",
            )

        if support_submitted:
            with st.spinner("Sending your request..."):
                process_customer_activity(support_query, support_loyalty_id)
            st.session_state["customer_confirmation"] = {"type": "support"}

confirmation = st.session_state.get("customer_confirmation")
if confirmation:
    st.space("medium")
    with st.container(border=True):
        if confirmation["type"] == "order":
            st.subheader("Order received", icon=":material/receipt_long:")
            st.write(f"{confirmation['quantity']} × {confirmation['item']}")
            st.metric("Estimated total", f"${confirmation['total']:.2f}")
            st.caption("This demo order has not been sent to a payment system.")
        else:
            st.subheader("Message received", icon=":material/mark_email_read:")
            st.write("Thanks for getting in touch. Our team will follow up with you.")