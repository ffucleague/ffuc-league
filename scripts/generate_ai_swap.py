import subprocess, sys, os, argparse, shutil, json, urllib.request, base64
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANAGERS_DIR = os.path.join(BASE_DIR, "assets", "managers")
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "video")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Load configuration from config.json with fallback defaults
config = {}
if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Notice loading config.json: {e}")

ai_cfg = config.get("ai_endpoints", {})
SERVER_HOST = ai_cfg.get("server_host", "192.168.86.67")
OLLAMA_URL = ai_cfg.get("ollama_url", f"http://{SERVER_HOST}:11434")
DEFAULT_VISION_MODEL = ai_cfg.get("default_vision_model", "qwen3-vl:32b")
LIVEPORTRAIT_URL = ai_cfg.get("liveportrait_url", f"http://{SERVER_HOST}:8890")
SSH_USER = "mark"

def query_vision_model(prompt, image_paths=None, model=DEFAULT_VISION_MODEL, timeout=120):
    """
    Queries the default Qwen3-VL:32B vision model on Ollama (http://192.168.86.67:11434)
    Supports multimodal input (images + text instructions).
    """
    print(f"\n🧠 Consulting Vision AI ({model}) at {OLLAMA_URL}...")
    images_b64 = []
    if image_paths:
        for p in image_paths:
            if os.path.exists(p):
                with open(p, "rb") as img_f:
                    b64 = base64.b64encode(img_f.read()).decode("utf-8")
                    images_b64.append(b64)
                    print(f"   🖼️ Attached image: {os.path.basename(p)}")
            else:
                print(f"   ⚠️ Warning: Image not found: {p}")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    if images_b64:
        payload["images"] = images_b64

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            response_text = data.get("response", "").strip()
            print(f"   💡 Vision AI Response:\n{response_text}\n")
            return response_text
    except Exception as e:
        print(f"   ⚠️ Vision AI query failed: {e}")
        return None

def analyze_meme_candidate(source_face, meme_template, model=DEFAULT_VISION_MODEL):
    """
    Uses Qwen3-VL:32B to evaluate the source manager face and meme video/gif template
    for face-swap suitability, expression matching, and comedic impact.
    """
    prompt = (
        "You are the visual meme director for the FFUC fantasy football league. "
        "Analyze these two visuals:\n"
        "Image 1: Manager source face\n"
        "Image 2: Driving meme template frame / gif\n"
        "Evaluate:\n"
        "1. Face angle and lighting compatibility for neural face-swapping\n"
        "2. Expression match (e.g. heartbreak crying vs celebration toast)\n"
        "3. Recommended crop and scale adjustments for the best realism\n"
        "Keep your advice sharp, concise, and actionable."
    )
    return query_vision_model(prompt, [source_face, meme_template], model=model)

def convert_video_to_gif(video_path, gif_path=None, fps=15, width=480):
    """
    Converts MP4 video to a high-quality looping GIF using ffmpeg
    """
    if not gif_path:
        gif_path = video_path.rsplit(".", 1)[0] + ".gif"
    
    print(f"\n🎞️ Converting {video_path} -> {gif_path} (FPS: {fps}, Width: {width})...")
    vf = f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", vf, gif_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        size_kb = os.path.getsize(gif_path) / 1024
        print(f"   ✅ GIF created successfully! ({size_kb:.1f} KB)")
        return gif_path
    except Exception as e:
        print(f"   ⚠️ FFmpeg conversion notice: {e}")
        return None

def run_liveportrait_swap(source_image, driving_video, output_name, make_gif=True, vision_check=True):
    """
    Executes portrait animation using LivePortrait WebUI at http://192.168.86.67:8890
    Optionally evaluates inputs with Qwen3-VL:32B and creates matching GIF.
    """
    os.makedirs(VIDEO_DIR, exist_ok=True)
    clean_out = output_name.replace('.mp4', '').replace('.gif', '')
    local_output = os.path.join(VIDEO_DIR, f"{clean_out}.mp4")
    
    print(f"\n🎬 Starting LivePortrait Animation via {LIVEPORTRAIT_URL}...")
    print(f"   Source face: {source_image}")
    print(f"   Driving video: {driving_video}")
    print(f"   Output destination: {local_output}")
    print(f"   Default Vision Model: {DEFAULT_VISION_MODEL}")
    
    if vision_check:
        print(f"   🔍 Pre-screening meme pairing with {DEFAULT_VISION_MODEL}...")
        try:
            analyze_meme_candidate(source_image, driving_video, model=DEFAULT_VISION_MODEL)
        except Exception as e:
            print(f"   (Vision screening skipped: {e})")

    try:
        from gradio_client import Client, handle_file
        print(f"   📡 Connecting to LivePortrait WebUI at {LIVEPORTRAIT_URL}...")
        client = Client(LIVEPORTRAIT_URL)
        
        source_file = handle_file(source_image)
        video_file = handle_file(driving_video)
        
        print("   ⚡ Running LivePortrait neural inference pipeline...")
        result = client.predict(
            param_0=source_file,
            param_1=video_file,
            param_2=video_file,
            param_3=source_file,
            param_4=source_file,
            param_5=False,  # normalize lip
            param_6=True,   # relative motion
            param_7=True,   # do crop (source)
            param_8=True,   # paste-back
            param_9=True,   # stitching
            param_10="all", # animation region
            param_11="expression-friendly", # driving option
            param_12=1.0,   # driving multiplier
            param_13=False, # do crop (driving)
            param_14=2.3,   # source crop scale
            param_15=0.0,   # source crop x
            param_16=-0.125,# source crop y
            param_17=2.2,   # driving crop scale
            param_18=0.0,   # driving crop x
            param_19=-0.1,  # driving crop y
            param_20=3e-07, # motion smooth strength
            param_21="",
            param_22="",
            api_name="/gpu_wrapped_execute_video"
        )
        
        output_video_path = None
        if isinstance(result, (list, tuple)):
            for item in result:
                if isinstance(item, dict) and 'video' in item:
                    output_video_path = item['video'].get('path')
                    if output_video_path and os.path.exists(output_video_path):
                        break
                elif isinstance(item, str) and item.endswith(('.mp4', '.mov', '.avi')) and os.path.exists(item):
                    output_video_path = item
                    break
        elif isinstance(result, str) and os.path.exists(result):
            output_video_path = result
            
        if output_video_path and os.path.exists(output_video_path):
            shutil.copyfile(output_video_path, local_output)
            file_size_mb = os.path.getsize(local_output) / (1024 * 1024)
            print(f"   🎉 LivePortrait generation complete! Saved {local_output} ({file_size_mb:.2f} MB)")
            
            if make_gif:
                convert_video_to_gif(local_output)
            return local_output
        else:
            print(f"   ⚠️ Could not extract video from response: {result}")
            
    except Exception as e:
        print(f"   ⚠️ Gradio API execution notice: {e}")
        print("   Attempting remote server SSH pipeline fallback...")
        
        try:
            remote_src = f"/tmp/{os.path.basename(source_image)}"
            remote_tgt = f"/tmp/{os.path.basename(driving_video)}"
            remote_out = f"/tmp/{clean_out}.mp4"
            
            print("   ⬆️ Uploading inputs to server...")
            subprocess.run(["scp", source_image, f"{SSH_USER}@{SERVER_HOST}:{remote_src}"], check=True)
            subprocess.run(["scp", driving_video, f"{SSH_USER}@{SERVER_HOST}:{remote_tgt}"], check=True)
            
            print("   ⚡ Triggering LivePortrait processing on host...")
            cmd = f"python3 -m liveportrait.run --source {remote_src} --driving {remote_tgt} --output {remote_out} || true"
            subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd], check=False)
            
            subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{remote_out}", local_output], check=False)
            if os.path.exists(local_output):
                file_size_mb = os.path.getsize(local_output) / (1024 * 1024)
                print(f"   🎉 LivePortrait complete via SSH! Saved {local_output} ({file_size_mb:.2f} MB)")
                if make_gif:
                    convert_video_to_gif(local_output)
                return local_output
        except Exception as ssh_err:
            print(f"   Notice on SSH fallback: {ssh_err}")

    return local_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"FFUC AI Video & GIF Generator (Default Vision: {DEFAULT_VISION_MODEL}, WebUI: {LIVEPORTRAIT_URL})")
    parser.add_argument("--source", help="Path to source face image (e.g. assets/managers/mark.jpg)")
    parser.add_argument("--target", help="Path to driving template video (e.g. template.mp4)")
    parser.add_argument("--output", default="ai_meme", help="Output name without extension")
    parser.add_argument("--model", default=DEFAULT_VISION_MODEL, help=f"Vision model name (default: {DEFAULT_VISION_MODEL})")
    parser.add_argument("--no-gif", action="store_true", help="Skip converting MP4 to GIF")
    parser.add_argument("--analyze", action="store_true", help="Analyze inputs using Qwen3-VL:32B vision AI")
    parser.add_argument("--list-managers", action="store_true", help="List all downloaded manager photos")
    parser.add_argument("--check-status", action="store_true", help="Check status of LivePortrait WebUI and Ollama Vision AI")
    
    args = parser.parse_args()
    
    if args.check_status:
        print("=== CHECKING AI SERVICES STATUS ===")
        # 1. LivePortrait WebUI
        try:
            resp = urllib.request.urlopen(LIVEPORTRAIT_URL, timeout=4)
            print(f"✅ LivePortrait WebUI is ONLINE at {LIVEPORTRAIT_URL} (Status: {resp.status})")
        except Exception as e:
            print(f"❌ LivePortrait WebUI at {LIVEPORTRAIT_URL}: {e}")
            
        # 2. Ollama Vision AI
        try:
            req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m['name'] for m in data.get('models', [])]
                print(f"✅ Ollama API is ONLINE at {OLLAMA_URL}")
                print(f"   🎯 Default Vision Model: {DEFAULT_VISION_MODEL}")
                print(f"   📦 Available models: {', '.join(models)}")
                if any(DEFAULT_VISION_MODEL in m for m in models):
                    print(f"   ⭐ {DEFAULT_VISION_MODEL} is downloaded and verified!")
                else:
                    print(f"   ⚠️ {DEFAULT_VISION_MODEL} not found in available tags")
        except Exception as e:
            print(f"❌ Ollama at {OLLAMA_URL}: {e}")
            
    elif args.list_managers:
        print("=== AVAILABLE MANAGER AVATARS ===")
        for f in os.listdir(MANAGERS_DIR):
            print(f"  • {f} ({os.path.join(MANAGERS_DIR, f)})")
            
    elif args.analyze and args.source and args.target:
        analyze_meme_candidate(args.source, args.target, model=args.model)
        
    elif args.source and args.target:
        run_liveportrait_swap(
            args.source,
            args.target,
            args.output,
            make_gif=not args.no_gif,
            vision_check=True
        )
    else:
        print(f"Default Vision Model configured: {DEFAULT_VISION_MODEL}")
        print("Usage:")
        print("  python scripts/generate_ai_swap.py --check-status")
        print("  python scripts/generate_ai_swap.py --source <face.jpg> --target <meme.mp4> --output <name>")
        print("  python scripts/generate_ai_swap.py --source <face.jpg> --target <meme.mp4> --analyze")
        print("  python scripts/generate_ai_swap.py --list-managers")
