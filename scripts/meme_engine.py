import os
import sys
import argparse
import json
import random
import subprocess
import base64
import urllib.request
import shutil

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MANAGERS_DIR = os.path.join(ASSETS_DIR, "managers")
VIDEO_DIR = os.path.join(ASSETS_DIR, "video")
TEMPLATES_DIR = os.path.join(ASSETS_DIR, "meme_templates")
CATALOG_PATH = os.path.join(TEMPLATES_DIR, "catalog.json")
HISTORY_PATH = os.path.join(TEMPLATES_DIR, "history.json")

SERVER_HOST = "192.168.86.67"
SSH_USER = "mark"
OLLAMA_URL = f"http://{SERVER_HOST}:11434"
VISION_MODEL = "qwen3-vl:32b"
CONTAINER_NAME = "732881ac44a7"
CONTAINER_TEMPLATE_DIR = "/facefusion/meme_templates"

def load_catalog():
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": {}}

def save_catalog(cat):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(hist):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2)

def list_templates():
    catalog = load_catalog()
    history = load_history()
    print("=" * 70)
    print("🎬 FFUC DYNAMIC MEME TEMPLATE CATALOG")
    print("=" * 70)
    
    for cat_key, cat_data in catalog.get("categories", {}).items():
        print(f"\n📁 Category: [{cat_key.upper()}] - {cat_data.get('display_name')}")
        print(f"   Target: {cat_data.get('target_award')}")
        templates = cat_data.get("templates", [])
        if not templates:
            print("   (No templates registered yet)")
            continue
        for idx, t in enumerate(templates, 1):
            t_id = t.get("id")
            # Check last used
            last_used = None
            for w in sorted(history.keys(), reverse=True):
                if history[w].get(cat_key, {}).get("template_id") == t_id:
                    mgr = history[w][cat_key].get("manager", "unknown")
                    last_used = f"{w} ({mgr})"
                    break
            last_str = f"Last Used: {last_used}" if last_used else "Never Used"
            print(f"   {idx}. ID: '{t_id}' | {t.get('title')} ({t.get('character')})")
            print(f"      File: {t.get('file')} | Vibe: {t.get('vibe')}")
            print(f"      Status: [{last_str}]")
    print("\n" + "=" * 70)

def pick_template(category, requested_id=None, avoid_last_n=1):
    catalog = load_catalog()
    cat_data = catalog.get("categories", {}).get(category)
    if not cat_data or not cat_data.get("templates"):
        raise ValueError(f"Category '{category}' has no templates registered in catalog.json")
    
    templates = cat_data["templates"]
    if requested_id:
        for t in templates:
            if t["id"] == requested_id:
                return t
        raise ValueError(f"Template ID '{requested_id}' not found in category '{category}'")
    
    history = load_history()
    recent_used = []
    # Collect recently used templates for this category
    for w in sorted(history.keys(), reverse=True)[:avoid_last_n]:
        used_id = history[w].get(category, {}).get("template_id")
        if used_id:
            recent_used.append(used_id)
            
    # Filter candidates
    available = [t for t in templates if t["id"] not in recent_used]
    if not available:
        available = templates # Fallback if all have been recently used
        
    chosen = random.choice(available)
    print(f"🎲 Selected template for {category}: '{chosen['id']}' ({chosen['title']})")
    return chosen

def query_vision_ai(prompt, image_path):
    print(f"\n🧠 Consulting Vision AI ({VISION_MODEL}) at {OLLAMA_URL}...")
    try:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        payload = {
            "model": VISION_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096
            },
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
    except Exception as e:
        print(f"⚠️ Vision AI check notice: {e}")
        return "Vision check skipped."

def run_meme_pipeline(category, manager, template_id=None, week=None, screen=True):
    print(f"\n🚀 Running FFUC Meme Pipeline for {category.upper()} -> Manager: {manager}")
    manager_jpg = os.path.join(MANAGERS_DIR, f"{manager.lower()}.jpg")
    if not os.path.exists(manager_jpg):
        raise FileNotFoundError(f"Manager avatar not found at {manager_jpg}")
    
    chosen_template = pick_template(category, requested_id=template_id)
    template_filename = chosen_template["file"]
    
    # 1. Sync files to container
    print("📦 Syncing assets to FaceFusion container...")
    container_source = f"/facefusion/{manager.lower()}.jpg"
    container_target = f"{CONTAINER_TEMPLATE_DIR}/{category}/{template_filename}"
    container_out = f"/facefusion/{manager.lower()}_{category}.mp4"
    
    # Copy manager face to container if not already there
    cmd_cp_mgr = f"docker cp '{manager_jpg}' {CONTAINER_NAME}:{container_source}"
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_cp_mgr], check=True)
    
    # 2. Run FaceFusion headless run
    print("⚡ Executing FaceFusion neural swap (CodeFormer + Hyperswap 1024 boost)...")
    cmd_ff = (
        f"docker exec {CONTAINER_NAME} python facefusion.py headless-run "
        f"-s '{container_source}' "
        f"-t '{container_target}' "
        f"-o '{container_out}' "
        f"--processors face_swapper face_enhancer "
        f"--face-swapper-model hyperswap_1a_256 "
        f"--face-swapper-pixel-boost 512x512 "
        f"--face-enhancer-model codeformer "
        f"--face-enhancer-blend 85 "
        f"--execution-providers cpu "
        f"--execution-thread-count 16"
    )
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_ff], check=True)
    
    # 3. Copy out from container to host /tmp
    host_mp4 = f"/tmp/{manager.lower()}_{category}.mp4"
    host_gif = f"/tmp/{manager.lower()}_{category}.gif"
    host_frame = f"/tmp/{manager.lower()}_{category}_frame.jpg"
    
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", f"docker cp {CONTAINER_NAME}:{container_out} {host_mp4}"], check=True)
    
    # 4. Extract verification frame
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", f"ffmpeg -y -ss 00:00:01.5 -i {host_mp4} -vframes 1 {host_frame}"], check=True)
    
    local_frame = os.path.join(VIDEO_DIR, f"{manager.lower()}_{category}_frame.jpg")
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{host_frame}", local_frame], check=True)
    
    if screen:
        prompt = (
            f"You are the visual meme director for the FFUC fantasy football league. "
            f"Critique this generated meme video frame for category '{category}' featuring manager '{manager}'. "
            f"Template: {chosen_template['title']}. "
            f"Evaluate facial alignment, realism, comedic timing, and provide a 1-10 quality score."
        )
        verdict = query_vision_ai(prompt, local_frame)
        print("\n" + "="*50)
        print("VISION AI QUALITY VERDICT:")
        print("="*50)
        print(verdict)
        print("="*50 + "\n")
        
    # 5. Convert to high-quality palette-optimized GIF
    print("🎞️ Generating optimized 256-color Lanczos GIF...")
    cmd_gif = (
        f"ffmpeg -y -i {host_mp4} "
        f"-vf 'fps=18,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5' "
        f"{host_gif}"
    )
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", cmd_gif], check=True)
    
    # 6. Download to assets/video/
    local_mp4 = os.path.join(VIDEO_DIR, f"{manager.lower()}_{category}.mp4")
    local_gif = os.path.join(VIDEO_DIR, f"{manager.lower()}_{category}.gif")
    
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{host_mp4}", local_mp4], check=True)
    subprocess.run(["scp", f"{SSH_USER}@{SERVER_HOST}:{host_gif}", local_gif], check=True)
    
    mp4_kb = os.path.getsize(local_mp4) / 1024
    gif_kb = os.path.getsize(local_gif) / 1024
    print(f"🎉 Complete! Saved:")
    print(f"   • {local_mp4} ({mp4_kb:.1f} KB)")
    print(f"   • {local_gif} ({gif_kb:.1f} KB)")
    
    # 7. Record to history
    if week:
        history = load_history()
        wk_key = f"week_{week}"
        if wk_key not in history:
            history[wk_key] = {}
        history[wk_key][category] = {
            "template_id": chosen_template["id"],
            "manager": manager.lower()
        }
        save_history(history)
        print(f"📝 Logged to history for Week {week}: {category} -> '{chosen_template['id']}'")

def add_template(file_path, category, template_id, title, character="", vibe=""):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source clip not found: {file_path}")
    
    catalog = load_catalog()
    if category not in catalog.get("categories", {}):
        raise ValueError(f"Category '{category}' does not exist in catalog")
    
    ext = os.path.splitext(file_path)[1]
    filename = f"{template_id}{ext}"
    target_local = os.path.join(TEMPLATES_DIR, category, filename)
    
    # Copy locally
    shutil.copyfile(file_path, target_local)
    print(f"✅ Saved local template: {target_local}")
    
    # Upload to server container
    remote_tmp = f"/tmp/{filename}"
    subprocess.run(["scp", file_path, f"{SSH_USER}@{SERVER_HOST}:{remote_tmp}"], check=True)
    subprocess.run(["ssh", f"{SSH_USER}@{SERVER_HOST}", f"docker cp {remote_tmp} {CONTAINER_NAME}:{CONTAINER_TEMPLATE_DIR}/{category}/{filename}"], check=True)
    print(f"✅ Uploaded template to FaceFusion container: {CONTAINER_TEMPLATE_DIR}/{category}/{filename}")
    
    # Update catalog
    entry = {
        "id": template_id,
        "file": filename,
        "title": title,
        "character": character,
        "vibe": vibe
    }
    # Check if ID exists, update or append
    cat_templates = catalog["categories"][category]["templates"]
    found = False
    for i, t in enumerate(cat_templates):
        if t["id"] == template_id:
            cat_templates[i] = entry
            found = True
            break
    if not found:
        cat_templates.append(entry)
    save_catalog(catalog)
    print(f"🎉 Catalog updated successfully for [{category.upper()}]: '{template_id}' ({title})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFUC Dynamic Meme Engine & Template Manager")
    parser.add_argument("--list", action="store_true", help="List all registered meme templates in catalog")
    parser.add_argument("--generate", action="store_true", help="Generate a meme for a manager and category")
    parser.add_argument("--category", choices=["high_roller", "heartbreak", "toilet_runner"], help="Award category")
    parser.add_argument("--manager", help="Manager name (e.g. herrador, robert, alex, pedro)")
    parser.add_argument("--template", help="Specific template ID (optional, auto-picks if omitted)")
    parser.add_argument("--week", type=int, help="Week number (optional, records to history)")
    parser.add_argument("--no-screen", action="store_true", help="Skip Qwen3-VL 32B visual screening")
    parser.add_argument("--add-template", help="Path to new template clip file to import")
    parser.add_argument("--id", help="Template ID for --add-template")
    parser.add_argument("--title", help="Template title for --add-template")
    parser.add_argument("--character", default="", help="Character name for --add-template")
    parser.add_argument("--vibe", default="", help="Vibe description for --add-template")
    
    args = parser.parse_args()
    
    if args.list:
        list_templates()
    elif args.add_template:
        if not args.category or not args.id or not args.title:
            print("Error: --add-template requires --category, --id, and --title")
            sys.exit(1)
        add_template(args.add_template, args.category, args.id, args.title, args.character, args.vibe)
    elif args.generate:
        if not args.category or not args.manager:
            print("Error: --generate requires --category and --manager")
            sys.exit(1)
        run_meme_pipeline(args.category, args.manager, template_id=args.template, week=args.week, screen=not args.no_screen)
    else:
        list_templates()
