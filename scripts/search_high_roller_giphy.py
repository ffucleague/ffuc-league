import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

queries = {
    "shaq_shimmy": [
        "https://giphy.com/gifs/shaq-shimmy-UO5elnTqo4vSg",
        "https://giphy.com/gifs/shaquille-oneal-nba-UO5elnTqo4vSg",
        "https://giphy.com/gifs/UO5elnTqo4vSg"
    ],
    "wolf_chest_thump": [
        "https://giphy.com/gifs/matthew-mcconaughey-the-wolf-of-wall-street-gBkBmnZkaWCnC",
        "https://giphy.com/gifs/leonardodicaprio-chest-thump-wolfofwallstreet-3o7TKF5DcqvQ5UT7Q4",
        "https://giphy.com/gifs/gBkBmnZkaWCnC"
    ],
    "ronaldo_siuuu": [
        "https://giphy.com/gifs/cristiano-ronaldo-siu-siuuu-R312C3MEVg4SCYAber",
        "https://giphy.com/gifs/football-celebration-ronaldo-hryis7A55UXIc",
        "https://giphy.com/gifs/R312C3MEVg4SCYAber"
    ],
    "conor_mcgregor_strut": [
        "https://giphy.com/gifs/ufc-mma-conor-mcgregor-3o6Zt4UC9H4sq5PqVy",
        "https://giphy.com/gifs/conor-mcgregor-strut-billionaire-3o6Zt4UC9H4sq5PqVy",
        "https://giphy.com/gifs/3o6Zt4UC9H4sq5PqVy"
    ]
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

high_roller_urls = {}

for name, candidates in queries.items():
    found = False
    for u in candidates:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
                mp4_match = re.search(r'https://media\d*\.giphy\.com/media/[^/]+/giphy\.mp4', html)
                v_url = og_video.group(1) if og_video else (mp4_match.group(0) if mp4_match else None)
                if v_url:
                    high_roller_urls[name] = v_url
                    print(f"✅ {name}: {v_url}")
                    found = True
                    break
        except Exception as e:
            continue
    if not found:
        print(f"❌ {name}: not found in list")

with open("scratch/high_roller_found.json", "w", encoding="utf-8") as f:
    json.dump(high_roller_urls, f, indent=2)
