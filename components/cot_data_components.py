import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_market_net_position(df, market_choice):
    df = df[df['Market_Names'] == market_choice]
    df_grouped = df.groupby('Date').agg({
        'NonComm_Long': 'sum',
        'NonComm_Short': 'sum'
    }).reset_index()

    df_grouped['Total'] = df_grouped['NonComm_Long'] + df_grouped['NonComm_Short']
    df_grouped['Long_Percentage'] = (df_grouped['NonComm_Long'] / df_grouped['Total']) * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df_grouped['Date'],
            y=df_grouped['NonComm_Long'],
            name='Long',
            marker_color='#2e8b57'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Bar(
            x=df_grouped['Date'],
            y=df_grouped['NonComm_Short'],
            name='Short',
            marker_color='#b22222'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df_grouped['Date'],
            y=df_grouped['Long_Percentage'],
            name='Long %',
            mode='lines',
            line=dict(color='yellow', width=2),
            line_shape='hv',

        ),
        secondary_y=True
    )

    fig.add_shape(
        type='line',
        x0=df_grouped['Date'].min(),
        x1=df_grouped['Date'].max(),
        y0=50,
        y1=50,
        line=dict(color='white', width=1, dash='dash'),
        xref='x',
        yref='y2'  # reference percentage axis
    )



    max_y = df_grouped[['NonComm_Long', 'NonComm_Short']].sum(axis=1).max()

    fig.update_layout(
        barmode='stack',
        title="Long vs Short Positions with Long % Overlay",
        height=450,
    )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total Positions", secondary_y=False, range=[0, max_y])
    fig.update_yaxes(title_text="Long %", secondary_y=True, range=[0, 100])
    fig.update_layout(
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        yaxis2_fixedrange=True,
    )
    st.plotly_chart(fig)
    show_table(df)


def plot_latest_date_overview(df):
    latest_date = df['Date'].max()
    df = df[df['Date'] == latest_date].copy()
    df['Percent_Long'] = df['NonComm_Long'] / df['Total']
    df['Percent_Short'] = df['NonComm_Short'] / df['Total']

    df_long = df.melt(
        id_vars='Market_Names',
        value_vars=['Percent_Long', 'Percent_Short'],
        var_name='Position_Type',
        value_name='Percent')

    df_long['Position_Type'] = df_long['Position_Type'].map({
        'Percent_Long': 'Long',
        'Percent_Short': 'Short'
    })

    color_map = {'Long': '#2e8b57', 'Short': '#b22222'}

    df_long = df_long.sort_values(by='Percent', ascending=False)

    fig = px.bar(
        df_long,
        x='Market_Names',
        y='Percent',
        color='Position_Type',
        color_discrete_map=color_map,
        title=f"Net Position Breakdown by Market on {latest_date}",
        labels={'Percent': 'Percent of Total'},
    )

    fig.update_layout(
        xaxis_title="Market Names",
        yaxis_title="Percentage of Net Position",
        yaxis=dict(range=[0, 1]),
        height=400,
        barmode='stack',
    )

    fig.add_shape(
        type="line",
        x0=-0.4, x1=len(df['Market_Names']),
        y0=0.5, y1=0.5,
        line=dict(color="white", width=1, dash="dash"),
        name="50% Line"
    )
    sorted_df = df.sort_values(by='Percent_Long', ascending=False)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig)

    with col2:
        show_table(sorted_df)

def show_table(df):
    st.dataframe(df[[
        'Market_Names', 'Date', 'NonComm_Long', 'NonComm_Short',
        'Change_Long', 'Change_Short', 'Net_Position'
    ]])