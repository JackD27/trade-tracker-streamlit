import streamlit as st

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

pip_calc_page = st.Page(
    page="views/pip_calc_view.py",
    title="Pip Calculator",
    icon="📱",
    default=False
)

pg = st.navigation({
    "Financials": [cot_page, trade_tracker_page],
    "Tools": [pip_calc_page]
})

st.set_page_config(
    page_title="Financial Tools",
    page_icon="??",
    layout="wide"
)

pg.run()