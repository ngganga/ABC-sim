import streamlit as st

import plotly.graph_objects as go

import plotly.express as px

from typing import List

import pandas as pd

from models import Decision, RoundResult, SimulationState

def display_metrics(results: List[RoundResult]):

if not results:

return

latest = results[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:

st.metric("Revenue", f"${latest.revenue:.1f}M", delta=f"{latest.revenue - (results[-2].revenue if len(results) > 1 else 0):.1f}M")

with col2:

st.metric("Profit", f"${latest.profit:.1f}M", delta=f"{latest.profit - (results[-2].profit if len(results) > 1 else 0):.1f}M")

with col3:

st.metric("Market Share", f"{latest.market_share:.1%}", delta=f"{(latest.market_share - (results[-2].market_share if len(results) > 1 else 0)):.1%}")

with col4:

st.metric("Cash Balance", f"${latest.cumulative_profit:.1f}M")

def create_decision_form(round_num: int) -> Decision:

st.header(f"Round {round_num} Decisions")

col1, col2 = st.columns(2)

with col1:

technology_investment = st.slider("Technology Investment ($M)", 0.0, 50.0, 10.0, 1.0)

marketing_budget = st.slider("Marketing Budget ($M)", 0.0, 30.0, 5.0, 1.0)

r_d_budget = st.slider("R&D Budget ($M)", 0.0, 20.0, 3.0, 1.0)

with col2:

pricing_strategy = st.selectbox("Pricing Strategy",

["premium", "competitive", "budget"],

index=1)

production_capacity = st.slider("Production Capacity (MW)", 10, 500, 100, 10)

if st.button("Submit Decisions", type="primary"):

return Decision(

round_number=round_num,

technology_investment=technology_investment,

marketing_budget=marketing_budget,

pricing_strategy=pricing_strategy,

production_capacity=production_capacity,

r_d_budget=r_d_budget

)

return None

def plot_financial_trends(results: List[RoundResult]):

if not results:

return

df = pd.DataFrame([{

'Round': r.round_number,

'Revenue': r.revenue,

'Profit': r.profit,

'Costs': r.costs,

'Cumulative Profit': r.cumulative_profit

} for r in results])

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['Round'], y=df['Revenue'], mode='lines+markers', name='Revenue'))

fig.add_trace(go.Scatter(x=df['Round'], y=df['Profit'], mode='lines+markers', name='Profit'))

fig.add_trace(go.Scatter(x=df['Round'], y=df['Costs'], mode='lines+markers', name='Costs'))

fig.update_layout(

title="Financial Performance Over Time",

xaxis_title="Round",

yaxis_title="Amount ($M)",

template="plotly_white"

)

st.plotly_chart(fig, use_container_width=True)

def plot_market_metrics(results: List[RoundResult]):

if not results:

return

df = pd.DataFrame([{

'Round': r.round_number,

'Market Share': r.market_share,

'Customer Satisfaction': r.customer_satisfaction,

'Technology Level': r.technology_level

} for r in results])

fig = go.Figure()

fig.add_trace(go.Scatter(x=df['Round'], y=df['Market Share'], mode='lines+markers', name='Market Share'))

fig.add_trace(go.Scatter(x=df['Round'], y=df['Customer Satisfaction'], mode='lines+markers', name='Customer Satisfaction'))

fig.add_trace(go.Scatter(x=df['Round'], y=df['Technology Level'], mode='lines+markers', name='Technology Level'))

fig.update_layout(

title="Market and Technology Metrics",

xaxis_title="Round",

yaxis_title="Score (0-1)",

template="plotly_white"

)

st.plotly_chart(fig, use_container_width=True)

def display_results_summary(results: List[RoundResult]):

if not results:

st.info("No results yet. Complete Round 1 to see results.")

return

st.header("Simulation Results Summary")

display_metrics(results)

st.divider()

col1, col2 = st.columns(2)

with col1:

plot_financial_trends(results)

with col2:

plot_market_metrics(results)

st.divider()

st.subheader("Detailed Results by Round")

results_df = pd.DataFrame([{

'Round': r.round_number,

'Revenue ($M)': f"{r.revenue:.1f}",

'Costs ($M)': f"{r.costs:.1f}",

'Profit ($M)': f"{r.profit:.1f}",

'Market Share': f"{r.market_share:.1%}",

'Customer Satisfaction': f"{r.customer_satisfaction:.2f}",

'Technology Level': f"{r.technology_level:.2f}",

'Cumulative Profit ($M)': f"{r.cumulative_profit:.1f}"

} for r in results])

st.dataframe(results_df, use_container_width=True)
