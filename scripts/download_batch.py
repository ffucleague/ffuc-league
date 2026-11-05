import os
import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

candidates = {
    # High Roller extra
    "shaq_shimmy": {
        "category": "high_roller",
        "url": "https://media2.giphy.com/media/UO5elnTqo4vSg/giphy.mp4",
        "title": "Shaq Shimmy Celebration",
        "character": "Shaquille O'Neal",
        "vibe": "Smug, shoulder shimmy victory bounce with big grin"
    },
    "wolf_chest_thump": {
        "category": "high_roller",
        "url": "https://media4.giphy.com/media/gdwJdym3VuXQr5OfAc/giphy.mp4",
        "title": "Wolf of Wall Street Chest Thump",
        "character": "Mark Hanna (Matthew McConaughey)",
        "vibe": "Rhythmic chest beating, humming, high roller Wall Street intensity"
    },
    
    # Heartbreak
    "michael_scott_heartbreak": {
        "category": "heartbreak",
        "url": "https://media1.giphy.com/media/pynZagVcYxVUk/giphy.mp4",
        "title": "Michael Scott Holding Back Tears",
        "character": "Michael Scott (Steve Carell)",
        "vibe": "Nodding, biting lip, trying desperately not to burst into tears"
    },
    "homelander_stress": {
        "category": "heartbreak",
        "url": "https://media1.giphy.com/media/5Nle87WgNwDbsj3P4Y/giphy.mp4",
        "title": "Homelander Psychotic Stress Stare",
        "character": "Homelander (Antony Starr)",
        "vibe": "Simmering rage, twitching eye, suppressed heartbreak and fury"
    },
    "dazn_waiting": {
        "category": "heartbreak",
        "url": "https://media1.giphy.com/media/G31qDpgbdpFPnGInD2/giphy.mp4",
        "title": "Sad Fan Waiting In Stasis",
        "character": "Sad Soccer Fan",
        "vibe": "Melancholy waiting, slumped over, devastated by defeat"
    },
    "spiderman_crying": {
        "category": "heartbreak",
        "url": "https://media2.giphy.com/media/hppWdK8gcmzXq/giphy.mp4",
        "title": "Peter Parker Spider-Man Crying",
        "character": "Peter Parker (Tobey Maguire)",
        "vibe": "Iconic grimacing weep, emotional devastation"
    },
    
    # Toilet Runner
    "frankie_lapenna_run": {
        "category": "toilet_runner",
        "url": "https://media3.giphy.com/media/shignv8uvl1Q65jP3s/giphy.mp4",
        "title": "Frankie LaPenna Power Sprint",
        "character": "Frankie LaPenna",
        "vibe": "High-speed frantic running with huge dump truck hips"
    },
    "hallway_sprint": {
        "category": "toilet_runner",
        "url": "https://media4.giphy.com/media/l1J3I2AACdYouQQec/giphy.mp4",
        "title": "Panic Hallway Sprint",
        "character": "Guy Sprinting Down Hallway",
        "vibe": "Pure terror, sprinting away through office hallways"
    },
    "panic_run_away": {
        "category": "toilet_runner",
        "url": "https://media4.giphy.com/media/2bUpP71bbVnZ3x7lgQ/giphy.mp4",
        "title": "Forrest Gump Football Field Sprint",
        "character": "Forrest Gump",
        "vibe": "Sprinting across the field without stopping, running out of the stadium"
    },
    "empty_wallet_broke": {
        "category": "toilet_runner",
        "url": "https://media4.giphy.com/media/NxJZnWD1RiWOCCwKgE/giphy.mp4",
        "title": "Empty Wallet Out of Cash",
        "character": "Struggling Guy with Wallet",
        "vibe": "Looking inside completely empty leather wallet with despair"
    },
    "paid_off_screaming": {
        "category": "toilet_runner",
        "url": "https://media0.giphy.com/media/vvVX3bHbb5ssswAzHq/giphy.mp4",
        "title": "Michael Torpey Panic Screaming",
        "character": "Michael Torpey",
        "vibe": "Agonized open-mouthed scream of financial doom and panic"
    }
}

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch", "candidate_clips")
os.makedirs(OUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

downloaded = {}
for name, data in candidates.items():
    mp4_path = os.path.join(OUT_DIR, f"{name}.mp4")
    print(f"📥 Downloading {name} ({data['category']})...")
    try:
        req = urllib.request.Request(data["url"], headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            with open(mp4_path, "wb") as f:
                f.write(content)
        size_kb = len(content) / 1024
        print(f"   Saved {name}.mp4 ({size_kb:.1f} KB)")
        data["local_mp4"] = mp4_path
        downloaded[name] = data
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")

with open(os.path.join(OUT_DIR, "batch_candidates.json"), "w", encoding="utf-8") as f:
    json.dump(downloaded, f, indent=2)

print(f"\n🎉 Successfully downloaded {len(downloaded)} / {len(candidates)} candidate clips!")
