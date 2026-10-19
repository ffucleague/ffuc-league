import subprocess, sys, os, argparse
sys.stdout.reconfigure(encoding='utf-8')

SERVER_HOST = "mark@192.168.86.67"
DOCKER_CONTAINER = "facefusion-docker-facefusion-rocm-1"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANAGERS_DIR = os.path.join(BASE_DIR, "assets", "managers")
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "video")

def run_face_swap(source_image, target_video, output_name):
    os.makedirs(VIDEO_DIR, exist_ok=True)
    clean_out = output_name.replace('.mp4', '')
    local_output = os.path.join(VIDEO_DIR, f"{clean_out}.mp4")
    
    print(f"\n🎬 Starting FaceFusion Swap on {SERVER_HOST}...")
    print(f"   Source face: {source_image}")
    print(f"   Target video: {target_video}")
    print(f"   Output destination: {local_output}")
    
    # 1. SCP source and target to server /tmp
    remote_src = f"/tmp/{os.path.basename(source_image)}"
    remote_tgt = f"/tmp/{os.path.basename(target_video)}"
    
    print("   ⬆️ Uploading inputs to server...")
    subprocess.run(["scp", source_image, f"{SERVER_HOST}:{remote_src}"], check=True)
    subprocess.run(["scp", target_video, f"{SERVER_HOST}:{remote_tgt}"], check=True)
    
    # 2. Copy inside docker container
    container_src = f"/facefusion/{os.path.basename(source_image)}"
    container_tgt = f"/facefusion/{os.path.basename(target_video)}"
    container_out = f"/facefusion/{clean_out}.mp4"
    
    ssh_setup = f"docker cp {remote_src} {DOCKER_CONTAINER}:{container_src} && docker cp {remote_tgt} {DOCKER_CONTAINER}:{container_tgt}"
    subprocess.run(["ssh", SERVER_HOST, ssh_setup], check=True)
    
    # 3. Execute FaceFusion ROCm inside container
    print("   ⚡ Running FaceFusion ROCm neural pipeline (this may take 1-2 minutes)...")
    ff_cmd = (
        f"docker exec {DOCKER_CONTAINER} python facefusion.py headless-run "
        f"-s {container_src} -t {container_tgt} -o {container_out} "
        f"--processors face_swapper face_enhancer --execution-providers rocm"
    )
    subprocess.run(["ssh", SERVER_HOST, ff_cmd], check=True)
    
    # 4. Extract from container to host /tmp and scp back to local
    remote_out = f"/tmp/{clean_out}.mp4"
    ssh_extract = f"docker cp {DOCKER_CONTAINER}:{container_out} {remote_out}"
    subprocess.run(["ssh", SERVER_HOST, ssh_extract], check=True)
    
    print(f"   ⬇️ Downloading finished swapped video to {local_output}...")
    subprocess.run(["scp", f"{SERVER_HOST}:{remote_out}", local_output], check=True)
    
    file_size_mb = os.path.getsize(local_output) / (1024 * 1024)
    print(f"   🎉 Face swap complete! Saved {local_output} ({file_size_mb:.2f} MB)")
    return local_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFUC FaceFusion Video Swapper CLI")
    parser.add_argument("--source", help="Path to source face image (e.g. assets/managers/guynamedpedro.jpg)")
    parser.add_argument("--target", help="Path to target template video (e.g. template.mp4)")
    parser.add_argument("--output", default="facefusion_meme", help="Output name without .mp4")
    parser.add_argument("--list-managers", action="store_true", help="List all downloaded manager photos")
    
    args = parser.parse_args()
    if args.list_managers:
        print("=== AVAILABLE MANAGER AVATARS ===")
        for f in os.listdir(MANAGERS_DIR):
            print(f"  • {f} ({os.path.join(MANAGERS_DIR, f)})")
    elif args.source and args.target:
        run_face_swap(args.source, args.target, args.output)
    else:
        print("Usage: python scripts/generate_ai_swap.py --source <image.jpg> --target <video.mp4> --output <name>")
        print("       python scripts/generate_ai_swap.py --list-managers")
