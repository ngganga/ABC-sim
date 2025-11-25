import streamlit as st

import pandas as pd

from datetime import datetime

from models import SimulationState, Decision

from simulation import SimulationEngine

from components import create_decision_form, display_results_summary

# Page configuration

st.set_page_config(

page_title="Clean Start Energy Simulation",

page_icon="⚡",

layout="wide",

initial_sidebar_state="expanded"

)

# Initialize session state

if 'simulation_state' not in st.session_state:

st.session_state.simulation_state = None

if 'simulation_engine' not in st.session_state:

st.session_state.simulation_engine = SimulationEngine()

def main():

st.title("⚡ Clean Start Energy Startup Simulation")

st.markdown("*Inspired by MIT Sloan School of Management*")

# Sidebar navigation

with st.sidebar:

st.header("Navigation")

page = st.radio("Go to:", ["Home", "Simulation", "Results"])

if st.session_state.simulation_state:

st.divider()

st.subheader("Simulation Status")

st.write(f"Company: {st.session_state.simulation_state.company_name}")

st.write(f"Current Round: {st.session_state.simulation_state.current_round}")

st.write(f"Cash Balance: ${st.session_state.simulation_state.cash_balance:.1f}M")

if page == "Home":

show_home_page()

elif page == "Simulation":

show_simulation_page()

elif page == "Results":

show_results_page()

def show_home_page():

st.header("Welcome to Clean Start Energy")

st.markdown("""

This simulation puts you in the role of a startup founder in the clean energy sector.

Your goal is to build a successful renewable energy company over 5 rounds of decision-making.

**Key Challenges:**

- Balance technology investment with market expansion

- Manage cash flow and profitability

- Compete in an evolving market

- Build customer satisfaction and market share

**How to Play:**

1. Start a new simulation by entering your company name

2. Make strategic decisions each round in the Simulation tab

3. View your progress and results in the Results tab

""")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:

company_name = st.text_input("Enter your company name:", placeholder="e.g., GreenPower Inc.")

if st.button("Start New Simulation", type="primary"):

if company_name.strip():

st.session_state.simulation_state = SimulationState(

company_name=company_name.strip(),

current_round=0,

cash_balance=100.0

)

st.success(f"Simulation started for {company_name}! Navigate to the Simulation tab to begin.")

st.rerun()

else:

st.error("Please enter a company name.")

with col2:

st.subheader("Game Rules")

st.markdown("""

- **5 Rounds**: Make decisions each round

- **Starting Cash**: $100M

- **Goal**: Maximize cumulative profit

- **Win Condition**: Positive cash flow and market leadership

""")

def show_simulation_page():

if not st.session_state.simulation_state:

st.warning("Please start a new simulation from the Home page first.")

return

state = st.session_state.simulation_state

if state.current_round >= state.total_rounds:

st.success("🎉 Simulation completed! Check the Results tab for your final performance.")

return

st.header(f"Round {state.current_round + 1} of {state.total_rounds}")

st.markdown(f"**Company:** {state.company_name}")

st.markdown(f"**Cash Balance:** ${state.cash_balance:.1f}M")

if state.results:

st.subheader("Previous Round Summary")

latest_result = state.results[-1]

col1, col2, col3 = st.columns(3)

with col1:

st.metric("Last Round Profit", f"${latest_result.profit:.1f}M")

with col2:

st.metric("Market Share", f"{latest_result.market_share:.1%}")

with col3:

st.metric("Technology Level", f"{latest_result.technology_level:.2f}")

st.divider()

decision = create_decision_form(state.current_round + 1)

if decision:

# Validate cash balance

total_cost = (decision.technology_investment + decision.marketing_budget +

decision.r_d_budget)

if total_cost > state.cash_balance:

st.error(f"Insufficient funds! Total cost: ${total_cost:.1f}M, Available: ${state.cash_balance:.1f}M")

return

# Process the decision

new_state = st.session_state.simulation_engine.run_simulation_round(state, decision)

st.session_state.simulation_state = new_state

st.success(f"Round {decision.round_number} completed! Results updated.")

st.rerun()

def show_results_page():

if not st.session_state.simulation_state:

st.warning("Please start a simulation first.")

return

state = st.session_state.simulation_state

display_results_summary(state.results)

if state.current_round >= state.total_rounds:

st.divider()

st.header("🏆 Final Results")

if state.results:

final_result = state.results[-1]

if final_result.cumulative_profit > 200:

st.success("Outstanding performance! You've built a highly successful energy company.")

elif final_result.cumulative_profit > 50:

st.info("Good job! Your company is profitable and growing.")

else:

st.warning("Your company needs more strategic decisions to succeed in the market.")

if __name__ == "__main__":

main()
