import json
with open("scripts/week6_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
pr = data.get("pickem_rosters", [])
print("pr len:", len(pr))
if pr:
    print(json.dumps(pr[0], indent=2))
