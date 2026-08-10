from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.agents.state import GenesisState
from src.agents.alert_monitor import check_alert
from src.agents.image_analyzer import check_image
from src.agents.response_planner import make_response_plan
from src.agents.quality_checker import check_plan
from src.agents.action_executor import run_actions

def alert_node(state:GenesisState)-> GenesisState:
    state["alert_info"] = check_alert(state["situation"])
    return state

def image_node(state:GenesisState)-> GenesisState:
    state["image_findings"] = check_image(state.get("image_path"))
    return state


def planner_node(state: GenesisState) -> GenesisState:
    disaster_type = state["alert_info"].get("disaster_type", "general")
    state["response_plan"] = make_response_plan(
        situation=state["situation"],
        disaster_type=disaster_type,
        alert_info=str(state["alert_info"]),
        image_findings=str(state["image_findings"]),
        location_hint=state["alert_info"].get("location_hint"),
    )
    return state

def checker_node(state: GenesisState) -> GenesisState:
    state["retry_count"] += 1
    state["quality_result"] = check_plan(state["response_plan"], state["situation"])
    return state


def executor_node(state: GenesisState) -> GenesisState:
    state["execution_result"] = run_actions(
        state["response_plan"],
        state["approved"],
        location_hint=state["alert_info"].get("location_hint"),
    )
    return state


def route_after_check(state: GenesisState) -> str:
    if state["quality_result"]["passed"]:
        return "executor"
    if state["retry_count"] >= 3:
        return "executor"
    return "planner"


builder = StateGraph(GenesisState)
builder.add_node("alert", alert_node)
builder.add_node("image", image_node)
builder.add_node("planner", planner_node)
builder.add_node("checker", checker_node)
builder.add_node("executor", executor_node)

builder.set_entry_point("alert")
builder.add_edge("alert", "image")
builder.add_edge("image", "planner")
builder.add_edge("planner", "checker")
builder.add_conditional_edges("checker", route_after_check, {"planner": "planner", "executor": "executor"})
builder.add_edge("executor", END)

memory = MemorySaver()
app = builder.compile(checkpointer=memory, interrupt_before=["executor"])