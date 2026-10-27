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

# Fetch weeks 1 through 7 matchups
weekly_matchups = {}
for w in range(1, 8):
    m_list = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{w}")
    weekly_matchups[w] = m_list
    for m in m_list:
        rid = m["roster_id"]
        roster_map[rid]["scores"].append(m.get("points", 0.0))

print("=== ALL-PLAY & LUCK INDEX THROUGH WEEK 7 ===")
# All-play: each week, compare score against all other 9 teams
all_play_records = {rid: {"wins": 0, "losses": 0, "ties": 0} for rid in roster_map}

for w in range(1, 8):
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
    expected_wins = ap_pct * 7.0
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
        "fpts_against": r["fpts_against"]
    })

luck_data.sort(key=lambda x: x["luck_diff"], reverse=True)
print(f"{'Manager':<12} {'Actual':<8} {'All-Play':<10} {'Exp Wins':<10} {'Luck Diff':<10} {'Verdict'}")
for ld in luck_data:
    verdict = "Lucky (+)" if ld["luck_diff"] > 0.5 else ("Unlucky (-)" if ld["luck_diff"] < -0.5 else "Neutral")
    print(f"{ld['manager_name']:<12} {ld['actual_record']:<8} {ld['all_play_record']:<10} {ld['expected_wins']:<10.2f} {ld['luck_diff']:>+8.2f}   {verdict}")

print("\n=== POWER RANKINGS THROUGH WEEK 7 ===")
# Composite Power Ranking Formula:
# PR Score = (Wins * 10) + (PF * 0.15) + (AllPlayPct * 40) + (Week7Score * 0.15) - (PA * 0.02)
for ld in luck_data:
    rid = ld["roster_id"]
    w7_score = roster_map[rid]["scores"][-1]
    pr_score = (ld["actual_wins"] * 10.0) + (ld["fpts"] * 0.15) + (ld["all_play_pct"] * 40.0) + (w7_score * 0.15) - (ld["fpts_against"] * 0.02)
    ld["pr_score"] = pr_score
    ld["w7_score"] = w7_score

pr_rankings = sorted(luck_data, key=lambda x: x["pr_score"], reverse=True)
for i, pr in enumerate(pr_rankings, 1):
    print(f"{i:>2}. {pr['manager_name']:<12} (Score: {pr['pr_score']:.2f}) — Rec: {pr['actual_record']} | PF: {pr['fpts']:.2f} | W7: {pr['w7_score']:.2f}")

# Fetch Week 8 Matchups
matchups8 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/8")
m8_groups = {}
for m in matchups8:
    mid = m["matchup_id"]
    if mid not in m8_groups: m8_groups[mid] = []
    rid = m["roster_id"]
    m8_groups[mid].append(roster_map[rid])

print("\n=== WEEK 8 UPCOMING MATCHUPS ===")
for mid, teams in m8_groups.items():
    if len(teams) == 2:
        print(f"Matchup {mid}: {teams[0]['manager_name']} ({teams[0]['wins']}-{teams[0]['losses']}) vs {teams[1]['manager_name']} ({teams[1]['wins']}-{teams[1]['losses']})")

# Fetch week 7 transactions (waivers)
tx_w7 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/7")
print(f"\n=== WEEK 7 TRANSACTIONS ({len(tx_w7)} total) ===")
waiver_moves = []
for t in tx_w7:
    ttype = t.get("type")
    status = t.get("status")
    adds = t.get("adds") or {}
    drops = t.get("drops") or {}
    bid = t.get("settings", {}).get("waiver_bid", 0) or 0
    creator_id = t.get("creator")
    # find roster_id
    rids = t.get("roster_ids", [])
    mgr_name = roster_map[rids[0]]["manager_name"] if rids and rids[0] in roster_map else "Unknown"
    waiver_moves.append({
        "type": ttype,
        "status": status,
        "manager": mgr_name,
        "bid": bid,
        "adds": list(adds.keys()),
        "drops": list(drops.keys())
    })
    print(f"[{status.upper()}] {mgr_name}: {ttype} | Bid: ${bid} | Adds: {list(adds.keys())} | Drops: {list(drops.keys())}")

with open("scripts/week7_stats_full.json", "w", encoding="utf-8") as f:
    json.dump({
        "luck_data": luck_data,
        "pr_rankings": pr_rankings,
        "waiver_moves": waiver_moves,
        "week8_matchups": [{
            "matchup_id": mid,
            "team1": teams[0]["manager_name"],
            "team2": teams[1]["manager_name"]
        } for mid, teams in m8_groups.items() if len(teams) == 2]
    }, f, indent=2)
print("\nSaved week7_stats_full.json successfully")
