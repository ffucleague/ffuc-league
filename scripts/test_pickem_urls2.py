import urllib.request, json

PICKEM_ID = "1402701854898450432"
# Robert's user_id: 1134279549320822784
uid = "1134279549320822784"
candidates = [
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks/6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks/v1:regular:6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks/v1:regular:5",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/picks",
    f"https://api.sleeper.app/v1/user/{uid}/picks",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/user/{uid}",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/score/6",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/scores",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/standings",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/leaderboards",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/bracket",
    f"https://api.sleeper.app/v1/league/{PICKEM_ID}/pools",
]

for url in candidates:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("FOUND:", url, "Type:", type(data), "Len:", len(data) if isinstance(data, (list, dict)) else data)
    except Exception as e:
        pass
