import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = {
    "wolf_chest_thump": [
        "https://giphy.com/gifs/leonardodicaprio-the-wolf-of-wall-street-gBkBmnZkaWCnC",
        "https://giphy.com/gifs/gBkBmnZkaWCnC",
        "https://giphy.com/gifs/reaction-cheering-mrw-gBkBmnZkaWCnC",
        "https://giphy.com/gifs/wolfofwallstreet-the-wolf-of-wall-street-chest-thump-3o7TKF5DcqvQ5UT7Q4"
    ],
    "ronaldo_siuuu": [
        "https://giphy.com/gifs/cristiano-ronaldo-siu-siuuu-R312C3MEVg4SCYAber",
        "https://giphy.com/gifs/champions-league-cr7-cristiano-ronaldo-R312C3MEVg4SCYAber",
        "https://giphy.com/gifs/siu-siuuu-ronaldo-3o6Zt6KHxJTbXCnSvu"
    ],
    "conor_mcgregor_strut": [
        "https://giphy.com/gifs/ufc-mma-conor-mcgregor-3o6Zt4UC9H4sq5PqVy",
        "https://giphy.com/gifs/conor-mcgregor-walk-strut-3o6Zt4UC9H4sq5PqVy",
        "https://giphy.com/gifs/ufc-conor-mcgregor-the-notorious-l0HlOBZRezdd8skqk"
    ]
}

results = {}

for name, urls in queries.items():
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
                if og_video:
                    results[name] = og_video.group(1)
                    print(f"✅ Found {name}: {og_video.group(1)}")
                    break
                mp4_match = re.search(r'https://media\d*\.giphy\.com/media/([a-zA-Z0-9]+)/giphy\.mp4', html)
                if mp4_match:
                    results[name] = mp4_match.group(0)
                    print(f"✅ Found {name} (mp4 match): {mp4_match.group(0)}")
                    break
        except Exception as e:
            continue
    if name not in results:
        print(f"❌ Not found directly: {name}")

with open("scratch/extra_high_roller.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
