import subprocess, sys, os, argparse, shutil
sys.stdout.reconfigure(encoding='utf-8')

LIVEPORTRAIT_URL = "http://192.168.86.67:8890"
SERVER_HOST = "mark@192.168.86.67"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANAGERS_DIR = os.path.join(BASE_DIR, "assets", "managers")
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "video")

def run_liveportrait_swap(source_image, driving_video, output_name):
    """
    Executes portrait animation using LivePortrait WebUI at http://192.168.86.67:8890
    """
    os.makedirs(VIDEO_DIR, exist_ok=True)
    clean_out = output_name.replace('.mp4', '')
    local_output = os.path.join(VIDEO_DIR, f"{clean_out}.mp4")
    
    print(f"\n🎬 Starting LivePortrait Animation via {LIVEPORTRAIT_URL}...")
    print(f"   Source face: {source_image}")
    print(f"   Driving video: {driving_video}")
    print(f"   Output destination: {local_output}")
    
    try:
        from gradio_client import Client, handle_file
        print(f"   📡 Connecting to LivePortrait WebUI at {LIVEPORTRAIT_URL}...")
        client = Client(LIVEPORTRAIT_URL)
        
        # Prepare inputs
        source_file = handle_file(source_image)
        video_file = handle_file(driving_video)
        
        print("   ⚡ Running LivePortrait neural inference pipeline...")
        # Call /gpu_wrapped_execute_video
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
            param_21="",    # parameter_44
            param_22="",    # parameter_67
            api_name="/gpu_wrapped_execute_video"
        )
        
        # The result returns a tuple of outputs; find the animated video path
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
            return local_output
        else:
            print(f"   ⚠️ Could not extract video from response: {result}")
            
    except Exception as e:
        print(f"   ⚠️ Gradio API execution notice: {e}")
        print("   Attempting remote server SSH pipeline fallback...")
        
        # Fallback via SSH/SCP if direct Gradio client encountered network issues
        try:
            remote_src = f"/tmp/{os.path.basename(source_image)}"
            remote_tgt = f"/tmp/{os.path.basename(driving_video)}"
            remote_out = f"/tmp/{clean_out}.mp4"
            
            print("   ⬆️ Uploading inputs to server...")
            subprocess.run(["scp", source_image, f"{SERVER_HOST}:{remote_src}"], check=True)
            subprocess.run(["scp", driving_video, f"{SERVER_HOST}:{remote_tgt}"], check=True)
            
            print("   ⚡ Triggering LivePortrait processing on host...")
            cmd = f"python3 -m liveportrait.run --source {remote_src} --driving {remote_tgt} --output {remote_out} || true"
            subprocess.run(["ssh", SERVER_HOST, cmd], check=False)
            
            subprocess.run(["scp", f"{SERVER_HOST}:{remote_out}", local_output], check=False)
            if os.path.exists(local_output):
                file_size_mb = os.path.getsize(local_output) / (1024 * 1024)
                print(f"   🎉 LivePortrait complete via SSH! Saved {local_output} ({file_size_mb:.2f} MB)")
                return local_output
        except Exception as ssh_err:
            print(f"   Notice on SSH fallback: {ssh_err}")

    return local_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFUC LivePortrait AI Video Generator CLI (WebUI: 192.168.86.67:8890)")
    parser.add_argument("--source", help="Path to source face image (e.g. assets/managers/guy_named_pedro.png)")
    parser.add_argument("--target", help="Path to driving template video (e.g. template.mp4)")
    parser.add_argument("--output", default="liveportrait_meme", help="Output name without .mp4")
    parser.add_argument("--list-managers", action="store_true", help="List all downloaded manager photos")
    parser.add_argument("--check-status", action="store_true", help="Check status of LivePortrait WebUI at 192.168.86.67:8890")
    
    args = parser.parse_args()
    if args.check_status:
        import urllib.request
        try:
            resp = urllib.request.urlopen(LIVEPORTRAIT_URL, timeout=4)
            print(f"✅ LivePortrait WebUI is ONLINE at {LIVEPORTRAIT_URL} (Status: {resp.status})")
        except Exception as e:
            print(f"❌ Could not reach LivePortrait WebUI at {LIVEPORTRAIT_URL}: {e}")
    elif args.list_managers:
        print("=== AVAILABLE MANAGER AVATARS ===")
        for f in os.listdir(MANAGERS_DIR):
            print(f"  • {f} ({os.path.join(MANAGERS_DIR, f)})")
    elif args.source and args.target:
        run_liveportrait_swap(args.source, args.target, args.output)
    else:
        print("Usage: python scripts/generate_ai_swap.py --source <image.png> --target <video.mp4> --output <name>")
        print("       python scripts/generate_ai_swap.py --check-status")
        print("       python scripts/generate_ai_swap.py --list-managers")
