import json
import urllib.request
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PICKEM_ID = "1402701854898450432"
def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

league = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}")
print("Pickem League:", league.get("name"), "Status:", league.get("status"))

users = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users")
user_map = {u["user_id"]: u.get("display_name") for u in users}

rosters = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/rosters")
print(f"Rosters count: {len(rosters)}")
for r in rosters:
    uid = r.get("owner_id")
    name = user_map.get(uid, f"User {uid}")
    print(f"Roster ID {r.get('roster_id')}: User {name}, Settings: {r.get('settings')}")

