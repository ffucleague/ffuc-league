import os
import sys
import subprocess
import json
import base64
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

SERVER_HOST = "192.168.86.67"
SSH_USER = "mark"
OLLAMA_URL = f"http://{SERVER_HOST}:11434"
VISION_MODEL = "qwen3-vl:32b"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATES_DIR = os.path.join(BASE_DIR, "scratch", "candidate_clips")
BATCH_FILE = os.path.join(CANDIDATES_DIR, "batch_candidates.json")

with open(BATCH_FILE, "r", encoding="utf-8") as f:
    candidates = json.load(f)

print(f"Loaded {len(candidates)} candidates.")

# 1. Fetch extracted frames and metadata
print("\n📥 Fetching extracted frames and metadata from server...")
for name in candidates:
    remote_meta = f"/tmp/candidate_clips/{name}_meta.json"
    remote_frame = f"/tmp/candidate_clips/{name}_frame.jpg"
    local_meta = os.path.join(CANDIDATES_DIR, f"{name}_meta.json")
    local_frame = os.path.join(CANDIDATES_DIR, f"{name}_frame.jpg")
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{remote_meta}", local_meta], check=True)
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{remote_frame}", local_frame], check=True)

# 2. Evaluate each with Qwen3-VL 32B
print(f"\n🧠 Screening candidate clips with {VISION_MODEL} (num_ctx: 4096)...")

def query_vision(prompt, img_path):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    payload = {
        "model": VISION_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096
        },
        "images": [b64]
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return res.get("response", "").strip()

evaluations = {}

for idx, (name, meta) in enumerate(candidates.items(), 1):
    cat = meta["category"]
    title = meta["title"]
    char = meta.get("character", "")
    frame_path = os.path.join(CANDIDATES_DIR, f"{name}_frame.jpg")
    local_meta = os.path.join(CANDIDATES_DIR, f"{name}_meta.json")
    
    with open(local_meta, "r", encoding="utf-8") as f:
        p_data = json.load(f).get("streams", [{}])[0]
    
    w = p_data.get("width", 0)
    h = p_data.get("height", 0)
    dur = p_data.get("duration", "N/A")
    
    prompt = (
        f"You are the visual meme director for the FFUC fantasy football league. "
        f"Analyze this image frame from candidate meme clip '{name}' ({w}x{h}, {dur}s) for category '{cat.upper()}'.\n"
        f"Candidate Title: {title} ({char})\n"
        f"Please evaluate:\n"
        f"1. Subject & Scene: Who/what is depicted?\n"
        f"2. Face Swap Feasibility: Is the primary face visible, well-lit, and front-facing? Are there sunglasses, hands, microphones, extreme motion blur, or obstructions covering the face?\n"
        f"3. Category Vibe Fit: How well does this fit the '{cat}' theme?\n"
        f"4. Final Verdict: Explicitly state [APPROVED], [CONDITIONALLY APPROVED], or [NOT RECOMMENDED] with a 1-sentence reason."
    )
    
    print(f"\n=======================================================")
    print(f"🎬 [{idx}/{len(candidates)}] Screening [{cat.upper()}] Candidate: '{name}' ({w}x{h})")
    print(f"=======================================================")
    
    review = query_vision(prompt, frame_path)
    evaluations[name] = {
        "category": cat,
        "title": title,
        "character": char,
        "vibe": meta.get("vibe", ""),
        "width": w,
        "height": h,
        "duration": dur,
        "review": review
    }
    print(review)

with open(os.path.join(CANDIDATES_DIR, "evaluations_summary.json"), "w", encoding="utf-8") as f:
    json.dump(evaluations, f, indent=2)

print("\n🎉 Evaluation complete! Saved to evaluations_summary.json")
