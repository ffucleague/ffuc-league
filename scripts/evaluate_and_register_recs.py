import os
import sys
import subprocess
import json
import base64
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

SERVER_HOST = "192.168.86.67"
SSH_USER = "mark"
OLLAMA_URL = f"http://{SERVER_HOST}:11434"
VISION_MODEL = "qwen3-vl:32b"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECS_DIR = os.path.join(BASE_DIR, "scratch", "recs_clips")
DOWNLOADED_FILE = os.path.join(RECS_DIR, "recs_downloaded.json")

sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
from meme_engine import add_template, list_templates

with open(DOWNLOADED_FILE, "r", encoding="utf-8") as f:
    clips = json.load(f)

print(f"Loaded {len(clips)} recommended candidate clips.")

# 1. Fetch frames and metadata locally
print("\n📥 Fetching extracted frames and metadata from server...")
for name in clips:
    remote_meta = f"/tmp/recs_clips/{name}_meta.json"
    remote_frame = f"/tmp/recs_clips/{name}_frame.jpg"
    local_meta = os.path.join(RECS_DIR, f"{name}_meta.json")
    local_frame = os.path.join(RECS_DIR, f"{name}_frame.jpg")
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{remote_meta}", local_meta], check=True)
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{remote_frame}", local_frame], check=True)

# 2. Screen with Qwen3-VL 32B
print(f"\n🧠 Screening clips with {VISION_MODEL} (num_ctx: 4096, num_predict: 800)...")

def query_vision(prompt, img_path):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    payload = {
        "model": VISION_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096,
            "num_predict": 800,
            "temperature": 0.2,
            "repeat_penalty": 1.15
        },
        "images": [b64]
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        resp_text = data.get("response", "").strip()
        thinking = data.get("thinking", "").strip()
        if not resp_text and thinking:
            return f"(From model thoughts): {thinking[-300:]}"
        return resp_text

approved_clips = []
rejected_clips = []

for idx, (name, info) in enumerate(clips.items(), 1):
    cat = info["category"]
    title = info["title"]
    char = info.get("character", "")
    frame_path = os.path.join(RECS_DIR, f"{name}_frame.jpg")
    local_meta = os.path.join(RECS_DIR, f"{name}_meta.json")
    
    with open(local_meta, "r", encoding="utf-8") as f:
        p_data = json.load(f).get("streams", [{}])[0]
        
    w = p_data.get("width", 0)
    h = p_data.get("height", 0)
    dur = p_data.get("duration", "N/A")
    
    prompt = (
        f"You are the visual meme director for the FFUC fantasy football league. "
        f"Analyze this image frame from candidate meme clip '{name}' ({w}x{h}, {dur}s) for category '{cat.upper()}'.\n"
        f"Candidate Title: {title} ({char})\n"
        f"1. Face Swap Feasibility: Is the primary face visible, well-lit, and suitable for FaceFusion face swapping? Note any sunglasses, extreme angles, or blur.\n"
        f"2. Comedic/Vibe Fit: Does it fit category '{cat}'?\n"
        f"3. Final Verdict: Explicitly state [APPROVED], [CONDITIONALLY APPROVED], or [NOT RECOMMENDED] with 1 concise sentence."
    )
    
    print(f"\n=======================================================")
    print(f"🎬 [{idx}/{len(clips)}] Screening [{cat.upper()}] Candidate: '{name}' ({w}x{h})")
    print(f"=======================================================")
    review = query_vision(prompt, frame_path)
    print(review)
    
    # Check verdict
    is_rejected = "[NOT RECOMMENDED]" in review or "[REJECTED]" in review
    if is_rejected:
        rejected_clips.append((name, info, review))
    else:
        approved_clips.append((name, info))

print(f"\nScreening Summary: {len(approved_clips)} Approved, {len(rejected_clips)} Rejected.")

# 3. Register approved templates into catalog and sync to FaceFusion container
print("\n=== Registering Approved Clips to Catalog & FaceFusion Container ===")
for name, info in approved_clips:
    print(f"Registering [{info['category'].upper()}] -> '{name}' ({info['title']})...")
    add_template(
        file_path=info["local_mp4"],
        category=info["category"],
        template_id=name,
        title=info["title"],
        character=info["character"],
        vibe=info["vibe"]
    )
    print("-" * 50)

print("\n🎉 All approved recommended clips registered and synced!")
list_templates()
