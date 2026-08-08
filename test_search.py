from src.agents.response_planner import make_response_plan
from src.agents.quality_checker import check_plan

plan = make_response_plan(
    situation="City flood, water rising fast in Zone A, hundreds trapped",
    disaster_type="flood",
)
result = check_plan(plan, situation="City flood, water rising fast in Zone A, hundreds trapped")
print(result)