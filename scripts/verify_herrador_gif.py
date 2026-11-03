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
MODEL = "qwen3-vl:32b"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "video")

def query_vision_ai(prompt, image_path):
    print(f"\n🧠 Consulting Vision AI ({MODEL}) at {OLLAMA_URL}...")
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "images": [img_b64]
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("response", "").strip()

def process_and_verify():
    print("=== Step 1: Copy from container to host /tmp ===")
    cmd_cp = f"docker cp 732881ac44a7:/facefusion/herrador_high_roller.mp4 /tmp/herrador_high_roller.mp4"
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_cp], check=True)
    
    print("=== Step 2: Extract verification frame and inspect properties ===")
    cmd_extract = (
        "ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,duration /tmp/herrador_high_roller.mp4; "
        "ffmpeg -y -ss 00:00:01.5 -i /tmp/herrador_high_roller.mp4 -vframes 1 /tmp/herrador_check_frame.jpg"
    )
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_extract], check=True)
    
    print("=== Step 3: Fetch frame locally for Qwen3-VL analysis ===")
    local_frame = os.path.join(VIDEO_DIR, "herrador_check_frame.jpg")
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/herrador_check_frame.jpg", local_frame], check=True)
    
    prompt = (
        "You are the visual quality evaluator for the FFUC fantasy football league. "
        "Analyze this generated video frame from the Week 8 High Roller Champion meme animation.\n"
        "Check:\n"
        "1. Is the face cleanly and naturally swapped onto the character (Great Gatsby raising a champagne glass)?\n"
        "2. Is the resolution, lighting, and facial blending clear and sharp without severe blur or distortion?\n"
        "3. Provide a brief verdict on whether this is a high-quality, hilarious celebration meme fit for the league site."
    )
    ai_verdict = query_vision_ai(prompt, local_frame)
    print("\n" + "="*50)
    print("VISION AI QUALITY VERDICT:")
    print("="*50)
    print(ai_verdict)
    print("="*50 + "\n")
    
    print("=== Step 4: Generate high-resolution optimized GIF on server ===")
    cmd_gif = (
        "ffmpeg -y -i /tmp/herrador_high_roller.mp4 "
        "-vf 'fps=18,scale=512:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5' "
        "/tmp/herrador_high_roller.gif"
    )
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_gif], check=True)
    
    print("=== Step 5: Download both MP4 and GIF to assets/video ===")
    local_mp4 = os.path.join(VIDEO_DIR, "herrador_high_roller.mp4")
    local_gif = os.path.join(VIDEO_DIR, "herrador_high_roller.gif")
    
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/herrador_high_roller.mp4", local_mp4], check=True)
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:/tmp/herrador_high_roller.gif", local_gif], check=True)
    
    mp4_size = os.path.getsize(local_mp4) / 1024
    gif_size = os.path.getsize(local_gif) / 1024
    print(f"✅ Success! Downloaded:\n  - {local_mp4} ({mp4_size:.1f} KB)\n  - {local_gif} ({gif_size:.1f} KB)")

if __name__ == "__main__":
    process_and_verify()
