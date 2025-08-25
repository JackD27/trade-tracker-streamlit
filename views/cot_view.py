import streamlit as st

from components.cot_data_components import plot_market_net_position, plot_latest_date_overview
from controllers.cot.cot_data import get_final_parsed_data_no_prev, update_final_parsed_data

df = get_final_parsed_data_no_prev("data/final_cot_data.csv")

st.title("Cot Data")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    market_type_choice = st.selectbox(label="Select Market Type",
                                      options=["All"] + sorted(df['Market_Type'].unique().tolist()),
                                      index=0)

with col2:
    if market_type_choice == "All":
        market_options = ["All"] + sorted(df['Market_Names'].unique().tolist())
    else:
        market_options = ["All"] + sorted(
            df.loc[df['Market_Type'] == market_type_choice, 'Market_Names'].unique().tolist())

    market_choice = st.selectbox(
        label="Select Market",
        options=market_options,
        index=0
    )


st.button("Refresh Data", on_click=lambda: update_final_parsed_data("data/final_cot_data.csv"))


if market_choice != "All":
    plot_market_net_position(df, market_choice)
else:
    plot_latest_date_overview(df)
