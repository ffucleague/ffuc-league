import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
PICKEM_ID = "1402701854898450432"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

users = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")

user_map = {}
for u in users:
    uid = u["user_id"]
    team_name = (u.get("metadata", {}).get("team_name") or u.get("display_name")).replace('\u200b', '').strip()
    user_map[uid] = {
        "display_name": u.get("display_name"),
        "team_name": team_name
    }

roster_map = {}
for r in rosters:
    rid = r["roster_id"]
    u = user_map.get(r["owner_id"], {})
    mgr_info = config.get("managers", {}).get(str(rid), {})
    fpts_int = r.get("settings", {}).get("fpts", 0)
    fpts_dec = r.get("settings", {}).get("fpts_decimal", 0)
    fpts_against_int = r.get("settings", {}).get("fpts_against", 0)
    fpts_against_dec = r.get("settings", {}).get("fpts_against_decimal", 0)
    fpts = float(f"{fpts_int}.{fpts_dec:02d}") if isinstance(fpts_dec, int) else float(f"{fpts_int}.{fpts_dec}")
    fpts_against = float(f"{fpts_against_int}.{fpts_against_dec:02d}") if isinstance(fpts_dec, int) else float(f"{fpts_against_int}.{fpts_against_dec}")
    waiver_budget = r.get("settings", {}).get("waiver_budget_used", 0)
    
    roster_map[rid] = {
        "roster_id": rid,
        "manager_name": mgr_info.get("name", u.get("display_name")),
        "team_name": u.get("team_name"),
        "wins": r.get("settings", {}).get("wins", 0),
        "losses": r.get("settings", {}).get("losses", 0),
        "fpts": fpts,
        "fpts_against": fpts_against,
        "faab_remaining": 100 - waiver_budget,
        "scores": []
    }

weekly_matchups = {}
for w in range(1, 9):
    m_list = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{w}")
    weekly_matchups[w] = m_list
    for m in m_list:
        rid = m["roster_id"]
        roster_map[rid]["scores"].append(m.get("points", 0.0))

print("=== ALL-PLAY & LUCK INDEX THROUGH WEEK 8 ===")
all_play_records = {rid: {"wins": 0, "losses": 0, "ties": 0} for rid in roster_map}

for w in range(1, 9):
    w_scores = [(m["roster_id"], m.get("points", 0.0)) for m in weekly_matchups[w]]
    for rid1, s1 in w_scores:
        for rid2, s2 in w_scores:
            if rid1 == rid2: continue
            if s1 > s2:
                all_play_records[rid1]["wins"] += 1
            elif s1 < s2:
                all_play_records[rid1]["losses"] += 1
            else:
                all_play_records[rid1]["ties"] += 1

luck_data = []
for rid, r in roster_map.items():
    ap = all_play_records[rid]
    ap_total = ap["wins"] + ap["losses"] + ap["ties"]
    ap_pct = ap["wins"] / ap_total if ap_total > 0 else 0.0
    expected_wins = ap_pct * 8.0
    actual_wins = r["wins"]
    luck_diff = actual_wins - expected_wins
    luck_data.append({
        "roster_id": rid,
        "manager_name": r["manager_name"],
        "team_name": r["team_name"],
        "actual_record": f"{r['wins']}-{r['losses']}",
        "all_play_record": f"{ap['wins']}-{ap['losses']}",
        "all_play_pct": ap_pct,
        "expected_wins": expected_wins,
        "actual_wins": actual_wins,
        "luck_diff": luck_diff,
        "fpts": r["fpts"],
        "fpts_against": r["fpts_against"],
        "faab_remaining": r["faab_remaining"]
    })

luck_data.sort(key=lambda x: x["luck_diff"], reverse=True)

print(f"{'Manager':10} | {'Actual':6} | {'All-Play':8} | {'Exp W':5} | {'Diff':5} | {'Luck Rating'}")
for l in luck_data:
    rating = "🍀 EXTREMELY LUCKY" if l['luck_diff'] >= 1.5 else "✨ LUCKY" if l['luck_diff'] > 0.4 else "💀 UNLUCKY" if l['luck_diff'] < -0.4 else "⚖️ NEUTRAL"
    print(f"{l['manager_name']:10} | {l['actual_record']:6} | {l['all_play_record']:8} | {l['expected_wins']:5.2f} | {l['luck_diff']:+5.2f} | {rating}")

# Power Rankings Calculation
# Blend of: 40% Points For, 30% All-Play Win %, 20% Actual Wins, 10% Last 3 Weeks Momentum
print("\n=== POWER RANKINGS THROUGH WEEK 8 ===")
max_pf = max(l["fpts"] for l in luck_data)
pr_list = []
for l in luck_data:
    rid = l["roster_id"]
    scores = roster_map[rid]["scores"]
    l3_avg = sum(scores[-3:]) / 3.0 if len(scores) >= 3 else sum(scores) / len(scores)
    
    pf_score = (l["fpts"] / max_pf) * 100
    ap_score = l["all_play_pct"] * 100
    win_score = (l["actual_wins"] / 8.0) * 100
    momentum_score = (l3_avg / (max_pf / 8.0)) * 100
    
    pr_score = (pf_score * 0.35) + (ap_score * 0.30) + (win_score * 0.20) + (momentum_score * 0.15)
    pr_list.append({
        "roster_id": rid,
        "manager_name": l["manager_name"],
        "team_name": l["team_name"],
        "record": l["actual_record"],
        "pr_score": pr_score,
        "fpts": l["fpts"],
        "all_play": l["all_play_record"],
        "l3_avg": l3_avg
    })

pr_list.sort(key=lambda x: x["pr_score"], reverse=True)
for i, p in enumerate(pr_list, 1):
    print(f"{i:2d}. {p['manager_name']:10} | Score: {p['pr_score']:5.1f} | Record: {p['record']} | PF: {p['fpts']:6.2f} | L3 Avg: {p['l3_avg']:5.1f}")

out_file = os.path.join(os.path.dirname(__file__), "luck_index_w8.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({
        "luck_data": luck_data,
        "power_rankings": pr_list,
        "all_play": all_play_records
    }, f, indent=2)
print(f"\nSaved {out_file} successfully")
