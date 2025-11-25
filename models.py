from pydantic import BaseModel

from typing import List, Optional

from datetime import datetime

class Decision(BaseModel):

round_number: int

technology_investment: float  # $ millions

marketing_budget: float  # $ millions

pricing_strategy: str  # "premium", "competitive", "budget"

production_capacity: int  # MW

r_d_budget: float  # $ millions

class RoundResult(BaseModel):

round_number: int

revenue: float

costs: float

profit: float

market_share: float

customer_satisfaction: float

technology_level: float

cash_flow: float

cumulative_profit: float

class SimulationState(BaseModel):

company_name: str

current_round: int

total_rounds: int = 5

decisions: List[Decision] = []

results: List[RoundResult] = []

cash_balance: float = 100.0  # Starting cash in $ millions

created_at: datetime = datetime.now()

updated_at: datetime = datetime.now()
