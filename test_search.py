from src.agents.alert_monitor import check_incoming

print(check_incoming(source="dataset", limit=3))
print(check_incoming(source="gdelt", query="flood", limit=3))