import streamlit as st
from controllers.trade_tracker.account_controller import AccountController

account_ctrl = AccountController()

# -----------------------------
# Create Account Form
# -----------------------------
def create_account_form():
    with st.form("create_account_form"):
        st.subheader("➕ Create New Portfolio Account")
        name = st.text_input("Account Name")
        initial_balance = st.number_input("Initial Balance", min_value=0.0, step=100.0)

        submit_account = st.form_submit_button("Create Account")

        if submit_account:
            if name.strip():
                acc = account_ctrl.create_account(name, initial_balance)
                st.success(f"✅ Created account: {acc.name} with balance {acc.current_balance}")
            else:
                st.error("⚠️ Please enter a valid account name.")

    # -----------------------------
    # List Accounts
    # -----------------------------
    st.subheader("💼 Accounts")
    accounts = account_ctrl.get_accounts()

    if not accounts:
        st.info("No accounts yet. Create one above.")
    else:
        for acc in accounts:
            st.markdown(f"**{acc.name}** — Balance: `{acc.current_balance}`")
