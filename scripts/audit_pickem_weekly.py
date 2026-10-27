import urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

PICKEM_ID = "1402701854898450432"
def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

users = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users")
user_map = {}
for u in users:
    uid = u["user_id"]
    user_map[uid] = u.get("display_name")

# Also map username to manager name
mgr_by_username = {}
for rid, info in config["managers"].items():
    mgr_by_username[info["username"].lower()] = info["name"]

print("==================================================")
print("       AUDITING PICK'EM WEEKLY WINNERS 1-7        ")
print("==================================================")

weekly_picks = {}
for w in range(1, 8):
    try:
        data = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks/{w}")
        weekly_picks[w] = data
    except Exception as e:
        print(f"Error fetching week {w}: {e}")

# Calculate weekly scores
for w in range(1, 8):
    picks = weekly_picks.get(w, [])
    scores = {}
    for p in picks:
        uid = p.get("user_id")
        scores[uid] = scores.get(uid, 0) + (1 if p.get("correct") is True else 0)
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_scores:
        top_score = sorted_scores[0][1]
        top_users = [u for u, s in sorted_scores if s == top_score]
        names = []
        for uid in top_users:
            uname = user_map.get(uid, uid)
            mname = mgr_by_username.get(uname.lower(), uname)
            names.append(f"{mname} ({uname})")
        print(f"Week {w} Pick-em Winner(s) [Score: {top_score}]: {', '.join(names)}")
