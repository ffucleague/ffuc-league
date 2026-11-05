import os
import sys
import json
import base64
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

SERVER_HOST = "192.168.86.67"
OLLAMA_URL = f"http://{SERVER_HOST}:11434"
VISION_MODEL = "qwen3-vl:32b"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATES_DIR = os.path.join(BASE_DIR, "scratch", "candidate_clips")

toilet_candidates = {
    "frankie_lapenna_run": {
        "title": "Frankie LaPenna Power Sprint",
        "character": "Frankie LaPenna",
        "vibe": "High-speed frantic running with exaggerated dump truck body"
    },
    "hallway_sprint": {
        "title": "Panic Hallway Sprint",
        "character": "Sprinting Office Guy",
        "vibe": "Panic escape through hallways looking back in fear"
    },
    "panic_run_away": {
        "title": "Forrest Gump Football Field Sprint",
        "character": "Forrest Gump",
        "vibe": "Sprinting endlessly down the football field in panic"
    },
    "empty_wallet_broke": {
        "title": "Empty Wallet Out of Cash",
        "character": "Struggling Guy with Wallet",
        "vibe": "Looking inside completely empty leather wallet with despair"
    },
    "paid_off_screaming": {
        "title": "Michael Torpey Panic Screaming",
        "character": "Michael Torpey",
        "vibe": "Agonized open-mouthed scream of financial panic"
    }
}

def query_vision(name, prompt, img_path):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Try first with balanced parameters
    params = [
        {"num_ctx": 4096, "num_predict": 300, "temperature": 0.6, "repeat_penalty": 1.15},
        {"num_ctx": 2048, "num_predict": 250, "temperature": 0.3, "repeat_penalty": 1.25}
    ]
    
    for attempt, opt in enumerate(params, 1):
        try:
            payload = {
                "model": VISION_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": opt,
                "images": [b64]
            }
            req = urllib.request.Request(
                f"{OLLAMA_URL}/api/generate",
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                return res.get("response", "").strip()
        except urllib.error.HTTPError as e:
            print(f"⚠️ Attempt {attempt} for '{name}' failed with HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} for '{name}' error: {e}")
            
    return "[ERROR] Unable to complete vision evaluation after retries."

evaluations = {}

for name, meta in toilet_candidates.items():
    frame_path = os.path.join(CANDIDATES_DIR, f"{name}_frame.jpg")
    meta_path = os.path.join(CANDIDATES_DIR, f"{name}_meta.json")
    
    with open(meta_path, "r", encoding="utf-8") as f:
        p_data = json.load(f).get("streams", [{}])[0]
        
    w = p_data.get("width", 0)
    h = p_data.get("height", 0)
    dur = p_data.get("duration", "N/A")
    
    prompt = (
        f"You are the visual meme director for the FFUC fantasy football league. "
        f"Analyze this frame from clip '{name}' ({w}x{h}, {dur}s) for the '5K Toilet Runner' award.\n"
        f"Title: {meta['title']} ({meta['character']})\n"
        f"Please provide:\n"
        f"1. Face Swap Feasibility: Is the face clear and unobstructed? Will FaceFusion detect and swap onto it reliably?\n"
        f"2. Comedic/Vibe Fit: Does it fit a manager running away in panic from last place or relegation?\n"
        f"3. Final Verdict: Explicitly state [APPROVED], [CONDITIONALLY APPROVED], or [NOT RECOMMENDED] with 1 concise sentence."
    )
    
    print(f"\n=======================================================")
    print(f"🏃 Evaluating Toilet Runner candidate: '{name}' ({w}x{h})")
    print(f"=======================================================")
    review = query_vision(name, prompt, frame_path)
    print(review)
    evaluations[name] = {
        "title": meta["title"],
        "character": meta["character"],
        "vibe": meta["vibe"],
        "width": w,
        "height": h,
        "duration": dur,
        "review": review
    }

with open(os.path.join(CANDIDATES_DIR, "toilet_runner_evaluations.json"), "w", encoding="utf-8") as f:
    json.dump(evaluations, f, indent=2)

print("\n🎉 Toilet Runner evaluations complete!")
