import streamlit as st

from models.base import get_engine_and_session

cot_page = st.Page(
    page="views/cot_view.py",
    title="Cot Data",
    icon="📊",
    default=True
)

trade_tracker_page = st.Page(
    page="views/trade_tracker_view.py",
    title="Trade Tracker",
    icon="💵",
    default=False
)

create_account_page = st.Page(
    page="views/create_account_view.py",
    title="Create Account",
    icon="🤵",
    default=False
)

pip_calc_page = st.Page(
    page="views/pip_calc_view.py",
    title="Pip Calculator",
    icon="📱",
    default=False
)

compound_interest_page = st.Page(
    page="views/compound_interest_view.py",
    title="Compound Interest",
    icon="📈",
    default=False
)

pg = st.navigation({
    "Financial Data": [cot_page],
    "Trade Tracker": [trade_tracker_page, create_account_page],
    "Tools": [pip_calc_page, compound_interest_page],
})

st.set_page_config(
    page_title="Financial Tools",
    page_icon="??",
    layout="wide"
)

# Initialize database connection
engine, SessionLocal = get_engine_and_session()
pg.run()