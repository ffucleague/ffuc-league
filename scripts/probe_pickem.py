import urllib.request, json
PICKEM_ID = "1402701854898450432"
candidates = [
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leaderboard",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/standings",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/scores",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/legs",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leg/v1:regular:6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/report",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/reports",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks/6",
]
for url in candidates:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("FOUND:", url, "Data:", type(data), len(data) if isinstance(data, (list, dict)) else data)
    except Exception as e:
        pass
print("Done probing")
