import urllib.request
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

candidates = {
    # High Roller
    "ronaldo_siu": {
        "category": "high_roller",
        "ids": ["hryis7A55UXZNCUTNA", "zpAFVPBydqN3P4LEn8", "dE4ANADtdJYiPN952s"],
        "title": "Cristiano Ronaldo SIU Celebration",
        "character": "Cristiano Ronaldo",
        "vibe": "Mid-air spin, landing with arms down, classic SIU victory roar"
    },
    "salt_bae": {
        "category": "high_roller",
        "ids": ["duXC6sgYKVGfE1LbK1", "dT3tIohkRjOEg", "j0FRul7DKU5kb2xEgY"],
        "title": "Salt Bae Gold Steak Seasoning",
        "character": "Salt Bae (Nusret Gökçe)",
        "vibe": "Flamboyant wrist flick sprinkling salt over luxury steak"
    },
    "ric_flair_wooo": {
        "category": "high_roller",
        "ids": ["Q9FGOQewX92eRRO9Qi", "yUI3a7RwLhOFy", "125WvQGXcU9bCE"],
        "title": "Ric Flair WOOOO Strut",
        "character": "Ric Flair",
        "vibe": "Flamboyant robe, strutting across the ring yelling WOOOO!"
    },
    
    # Heartbreak
    "jordan_crying": {
        "category": "heartbreak",
        "ids": ["t5qY8FyyM85a0", "r3al4VcoRYTde", "wuoxwsJbyPoxW"],
        "title": "Michael Jordan Crying Face",
        "character": "Michael Jordan",
        "vibe": "Tears streaming down, Hall of Fame weeping expression"
    },
    "walter_white_collapse": {
        "category": "heartbreak",
        "ids": ["ngEYWg5UOm6fa5MQRB", "t8QSeqwoy0Ol2", "kj8M1xRRriY3m"],
        "title": "Walter White Desert Collapse",
        "character": "Walter White (Bryan Cranston)",
        "vibe": "Falling to the desert ground in sheer shock and heartbreak"
    },
    "ben_affleck_smoking": {
        "category": "heartbreak",
        "ids": ["Sv0uzXvg8svM4", "1RaGAz2p13Wpo7kI2L", "9V8YhvMvJWOoBCjl1d"],
        "title": "Ben Affleck Exhausted Smoking",
        "character": "Ben Affleck",
        "vibe": "Smoking cigarette with closed eyes, utterly drained and stressed"
    },
    
    # Toilet Runner
    "indiana_jones_boulder": {
        "category": "toilet_runner",
        "ids": ["ckjhCBC8CnfO4SksRm", "RU5NGFfwTQ5C7SGeId", "zUOSSh0IE4Rag6ssR8"],
        "title": "Indiana Jones Boulder Sprint",
        "character": "Indiana Jones (Harrison Ford)",
        "vibe": "Sprinting down temple cave running away from giant rolling boulder"
    },
    "phoebe_running": {
        "category": "toilet_runner",
        "ids": ["j2MiuvFOw6Fby3L2LO", "hsn1wnk0RFLzFiJlVa", "Kfr7detSN4dGnkRBMo"],
        "title": "Phoebe Buffay Wild Central Park Run",
        "character": "Phoebe Buffay (Lisa Kudrow)",
        "vibe": "Flailing arms, wild unhinged running style through the park"
    },
    "jack_sparrow_run": {
        "category": "toilet_runner",
        "ids": ["foRFhpgC0HlFDfgQLt", "2xzMDvy94jON4U55tL"],
        "title": "Captain Jack Sparrow Beach Run",
        "character": "Captain Jack Sparrow (Johnny Depp)",
        "vibe": "Flailing hands sprinting down the beach running away in terror"
    }
}

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch", "recs_clips")
os.makedirs(OUT_DIR, exist_ok=True)

valid_downloads = {}

for name, info in candidates.items():
    print(f"\nProcessing '{name}'...")
    found = False
    for gid in info["ids"]:
        # Try both media.giphy.com and mediaX.giphy.com
        urls_to_try = [
            f"https://media.giphy.com/media/{gid}/giphy.mp4",
            f"https://media1.giphy.com/media/{gid}/giphy.mp4",
            f"https://media2.giphy.com/media/{gid}/giphy.mp4",
            f"https://media3.giphy.com/media/{gid}/giphy.mp4",
            f"https://media4.giphy.com/media/{gid}/giphy.mp4"
        ]
        for url in urls_to_try:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    if resp.getcode() == 200:
                        content = resp.read()
                        if len(content) > 10000: # at least 10KB
                            mp4_path = os.path.join(OUT_DIR, f"{name}.mp4")
                            with open(mp4_path, "wb") as f:
                                f.write(content)
                            print(f"   ✅ Downloaded {name} from {url} ({len(content)/1024:.1f} KB)")
                            valid_downloads[name] = {
                                "category": info["category"],
                                "title": info["title"],
                                "character": info["character"],
                                "vibe": info["vibe"],
                                "giphy_id": gid,
                                "url": url,
                                "local_mp4": mp4_path
                            }
                            found = True
                            break
            except Exception as e:
                continue
        if found:
            break
    if not found:
        print(f"   ❌ Could not download any working MP4 for '{name}'")

with open(os.path.join(OUT_DIR, "recs_downloaded.json"), "w", encoding="utf-8") as f:
    json.dump(valid_downloads, f, indent=2)

print(f"\n🎉 Successfully downloaded {len(valid_downloads)} / {len(candidates)} recommended candidate clips!")
