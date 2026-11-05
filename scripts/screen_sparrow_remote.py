import urllib.request
import json
import base64
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meme_engine import add_template

SERVER_HOST = "192.168.86.67"
SSH_USER = "mark"
OLLAMA_URL = f"http://{SERVER_HOST}:11434"
VISION_MODEL = "qwen3-vl:32b"

# Download /tmp/sparrow.mp4 and /tmp/sparrow_frame.jpg
local_mp4 = "scratch/recs_clips/jack_sparrow_run.mp4"
local_frame = "scratch/recs_clips/jack_sparrow_frame.jpg"

subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/sparrow.mp4", local_mp4], check=True)
subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/sparrow_frame.jpg", local_frame], check=True)

with open(local_frame, "rb") as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': VISION_MODEL,
    'prompt': 'Who is in this image? Is it Captain Jack Sparrow running on the beach? Is his face clear for face swap? Give verdict: [APPROVED] or [REJECTED].',
    'stream': False,
    'options': {'num_ctx': 4096, 'num_predict': 400, 'temperature': 0.1},
    'images': [b64]
}
req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=60) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    review = data.get("response") or data.get("thinking", "")
    print("Verdict:", review)

if "[APPROVED]" in review or "Jack Sparrow" in review:
    print("Adding Jack Sparrow run to toilet_runner...")
    add_template(
        file_path=local_mp4,
        category="toilet_runner",
        template_id="jack_sparrow_run",
        title="Captain Jack Sparrow Beach Sprint",
        character="Captain Jack Sparrow (Johnny Depp)",
        vibe="Flailing hands sprinting down the beach running away in terror"
    )
