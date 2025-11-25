import random

from typing import Dict, List

from models import Decision, RoundResult, SimulationState

class Market:

def __init__(self):

self.total_market_size = 1000  # MW

self.base_price_per_mw = 2.5  # $ millions per MW

self.competition_level = 0.5  # 0-1 scale

self.environmental_awareness = 0.6  # 0-1 scale

def get_demand_multiplier(self, round_num: int) -> float:

# Demand grows over time with some randomness

base_growth = 1.0 + (round_num - 1) * 0.1

random_factor = random.uniform(0.9, 1.1)

return base_growth * random_factor

def get_price_premium(self, technology_level: float) -> float:

# Higher technology allows premium pricing

return 1.0 + technology_level * 0.3

class Company:

def __init__(self, name: str):

self.name = name

self.technology_level = 0.5  # 0-1 scale

self.brand_strength = 0.3  # 0-1 scale

self.production_capacity = 50  # MW

self.cumulative_investment = 0.0

def update_from_decision(self, decision: Decision):

# Update technology level based on R&D investment

tech_improvement = decision.r_d_budget * 0.1

self.technology_level = min(1.0, self.technology_level + tech_improvement)

# Update brand strength based on marketing

brand_improvement = decision.marketing_budget * 0.05

self.brand_strength = min(1.0, self.brand_strength + brand_improvement)

# Update production capacity

self.production_capacity = decision.production_capacity

# Track cumulative investment

self.cumulative_investment += decision.technology_investment

class SimulationEngine:

def __init__(self):

self.market = Market()

def calculate_round_result(self, state: SimulationState, decision: Decision) -> RoundResult:

company = Company(state.company_name)

# Update company with all previous decisions

for prev_decision in state.decisions:

company.update_from_decision(prev_decision)

company.update_from_decision(decision)

# Calculate market dynamics

demand_multiplier = self.market.get_demand_multiplier(decision.round_number)

price_premium = self.market.get_price_premium(company.technology_level)

# Determine pricing based on strategy

if decision.pricing_strategy == "premium":

price_multiplier = price_premium

elif decision.pricing_strategy == "competitive":

price_multiplier = 1.0

else:  # budget

price_multiplier = 0.8

price_per_mw = self.market.base_price_per_mw * price_multiplier * demand_multiplier

# Calculate market share based on various factors

base_market_share = 0.1  # Starting point

tech_factor = company.technology_level * 0.3

brand_factor = company.brand_strength * 0.2

capacity_factor = min(1.0, company.production_capacity / self.market.total_market_size)

competition_penalty = self.market.competition_level * 0.1

market_share = min(0.8, base_market_share + tech_factor + brand_factor + capacity_factor - competition_penalty)

# Calculate financials

revenue = market_share * self.market.total_market_size * price_per_mw

costs = (decision.technology_investment + decision.marketing_budget +

decision.r_d_budget + company.production_capacity * 0.1)  # Operational costs

profit = revenue - costs

# Update cash balance

new_cash_balance = state.cash_balance + profit

# Calculate customer satisfaction

customer_satisfaction = (company.technology_level * 0.4 +

company.brand_strength * 0.3 +

(1 - abs(price_multiplier - 1.0)) * 0.3)

# Calculate cumulative profit

cumulative_profit = sum(result.profit for result in state.results) + profit

return RoundResult(

round_number=decision.round_number,

revenue=revenue,

costs=costs,

profit=profit,

market_share=market_share,

customer_satisfaction=customer_satisfaction,

technology_level=company.technology_level,

cash_flow=profit,

cumulative_profit=cumulative_profit

)

def run_simulation_round(self, state: SimulationState, decision: Decision) -> SimulationState:

result = self.calculate_round_result(state, decision)

# Update state

new_state = state.copy()

new_state.decisions.append(decision)

new_state.results.append(result)

new_state.cash_balance += result.profit

new_state.current_round = decision.round_number

new_state.updated_at = datetime.now()

return new_state
