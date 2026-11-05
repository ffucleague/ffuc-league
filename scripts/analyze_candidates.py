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

clips = [
    "vince_mcmahon_strut",
    "celebration_kid",
    "mason_ramsey_dance",
    "cheers_toast",
    "mls_boss_sunglasses"
]

print("=== Step 1: Upload clips to server /tmp/candidate_clips ===")
subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", "mkdir -p /tmp/candidate_clips"], check=True)
for c in clips:
    local_mp4 = os.path.join(CANDIDATES_DIR, f"{c}.mp4")
    subprocess.run(["scp", local_mp4, f"{SSH_USER}@{SERVER_HOST}:/tmp/candidate_clips/{c}.mp4"], check=True)

print("\n=== Step 2: Probe clips and extract frames on server ===")
probe_cmd = """
cd /tmp/candidate_clips
for f in *.mp4; do
    base=$(basename "$f" .mp4)
    ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration,nb_frames,r_frame_rate -of json "$f" > "${base}_meta.json"
    ffmpeg -y -ss 00:00:01 -i "$f" -vframes 1 "${base}_frame.jpg" 2>/dev/null || ffmpeg -y -i "$f" -vframes 1 "${base}_frame.jpg" 2>/dev/null
done
"""
subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", probe_cmd], check=True)

print("\n=== Step 3: Fetch frames and metadata locally ===")
for c in clips:
    meta_path = os.path.join(CANDIDATES_DIR, f"{c}_meta.json")
    frame_path = os.path.join(CANDIDATES_DIR, f"{c}_frame.jpg")
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/candidate_clips/{c}_meta.json", meta_path], check=True)
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/candidate_clips/{c}_frame.jpg", frame_path], check=True)

print("\n=== Step 4: Screen candidates with Qwen3-VL 32B ===")
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
for c in clips:
    frame_path = os.path.join(CANDIDATES_DIR, f"{c}_frame.jpg")
    meta_path = os.path.join(CANDIDATES_DIR, f"{c}_meta.json")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f).get("streams", [{}])[0]
        
    w = meta.get("width")
    h = meta.get("height")
    dur = meta.get("duration")
    
    prompt = (
        f"You are the visual meme director for the FFUC fantasy football league. "
        f"Analyze this image frame from candidate meme clip '{c}' ({w}x{h}, {dur}s) for the 'High Roller Champion' award.\n"
        f"Evaluate:\n"
        f"1. Who/what is shown in the frame?\n"
        f"2. Face Swap Feasibility: Is the face clear, front-facing, and unobscured? Are there sunglasses, hands, or fast blur that will break FaceFusion or YOLO face detection?\n"
        f"3. High Roller Vibe & Comedic Value: Does it fit a fantasy manager who just dropped the league's highest score?\n"
        f"4. Final Recommendation: [APPROVED], [CONDITIONALLY APPROVED], or [NOT RECOMMENDED] with a brief 1-2 sentence reason."
    )
    print(f"\n--- Evaluating '{c}' with {VISION_MODEL} ---")
    review = query_vision(prompt, frame_path)
    evaluations[c] = {
        "width": w,
        "height": h,
        "duration": dur,
        "review": review
    }
    print(review)

with open(os.path.join(CANDIDATES_DIR, "evaluations.json"), "w", encoding="utf-8") as f:
    json.dump(evaluations, f, indent=2)

print("\nFinished all candidate evaluations!")
