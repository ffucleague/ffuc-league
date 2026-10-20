import urllib.request, json
PICKEM_ID = "1402701854898450432"
candidates = [
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/report/v1:regular:5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/report/v1:regular:6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/reports/v1:regular:5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/v1:regular:5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/v1:regular:6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/leg/v1:regular:5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/leaderboard",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/scores",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/standings",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/reports",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pickem/picks",
]
for url in candidates:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("FOUND:", url, "Type:", type(data), "Data:", str(data)[:100])
    except Exception as e:
        pass
print("Done probing 2")
