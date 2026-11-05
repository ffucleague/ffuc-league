import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls = {
    # User's Heartbreak links
    "michael_scott_heartbreak": "https://giphy.com/gifs/the-office-michael-heartbreak-pynZagVcYxVUk",
    "homelander_stress": "https://giphy.com/gifs/stress-homelander-stresss-5Nle87WgNwDbsj3P4Y",
    "dazn_waiting": "https://giphy.com/gifs/dazn-reaction-waiting-wait-G31qDpgbdpFPnGInD2",
    "spiderman_crying": "https://giphy.com/gifs/crying-spider-man-actors-hppWdK8gcmzXq",
    
    # User's Toilet runner links
    "frankie_lapenna_run": "https://giphy.com/gifs/frankie-lapenna-frankielap-shignv8uvl1Q65jP3s",
    "hallway_sprint": "https://giphy.com/gifs/running-run-l1J3I2AACdYouQQec",
    "panic_run_away": "https://giphy.com/gifs/reaction-2bUpP71bbVnZ3x7lgQ",
    "empty_wallet_broke": "https://giphy.com/gifs/broke-no-money-empty-wallet-NxJZnWD1RiWOCCwKgE",
    "paid_off_screaming": "https://giphy.com/gifs/paidoff-trutv-paid-off-michael-torpey-vvVX3bHbb5ssswAzHq",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

results = {}

for name, u in urls.items():
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
            og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            mp4_match = re.search(r'https://media\d*\.giphy\.com/media/[^/]+/giphy\.mp4', html)
            
            v_url = og_video.group(1) if og_video else (mp4_match.group(0) if mp4_match else None)
            results[name] = {
                "title": og_title.group(1) if og_title else name,
                "video_url": v_url,
                "image_url": og_img.group(1) if og_img else None
            }
            print(f"✅ {name}: {v_url}")
    except Exception as e:
        print(f"❌ {name}: {e}")

with open("scratch/scraped_giphy_urls.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
