import urllib.request, urllib.parse, json, sys, time, os, argparse, re
sys.stdout.reconfigure(encoding='utf-8')

ALLTALK_BASE_URL = "http://192.168.86.67:7851"
DEFAULT_OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio")

def sanitize_for_tts(text):
    """
    Cleans text for XTTSv2 / AllTalk to prevent hallucination and audio glitching:
    - Normalizes acronyms and hyphens in compound words
    - Expands currency ($10 -> ten dollar)
    - Expands numbers (e.g. 5K -> five K, Week 6 -> Week six)
    - Cleans abrupt question marks and odd characters
    """
    t = text
    t = re.sub(r'\$([0-9]+)', r'\1 dollar', t)
    t = re.sub(r'\b5K\b', 'five K', t, flags=re.IGNORECASE)
    t = re.sub(r'\bPick-Em\b|\bPick-em\b', 'pick em', t, flags=re.IGNORECASE)
    t = re.sub(r'\bWeek\s*([0-9]+)\b', lambda m: f"Week {['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen'][int(m.group(1))]}" if int(m.group(1)) <= 18 else m.group(0), t, flags=re.IGNORECASE)
    t = t.replace('?', ',')
    return t

def list_voices():
    try:
        url = f"{ALLTALK_BASE_URL}/api/voices"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("=== AVAILABLE ALLTALK VOICES ===")
            for v in data.get('voices', []):
                print(f"  • {v}")
    except Exception as e:
        print(f"Error fetching voices: {e}")

def generate_audio(text, voice="Morgan_Freeman CC3.wav", output_name="custom_broadcast"):
    os.makedirs(DEFAULT_OUT_DIR, exist_ok=True)
    clean_output_name = output_name.replace('.wav', '')
    sanitized_text = sanitize_for_tts(text)
    
    print(f"\n🎙️ Connecting to AllTalk TTS at {ALLTALK_BASE_URL}...")
    print(f"   Voice: {voice}")
    print(f"   Output: {clean_output_name}.wav")
    print(f"   Original Text ({len(text)} chars): \"{text[:70]}...\"")
    print(f"   Sanitized Text: \"{sanitized_text[:70]}...\"")
    
    payload = {
        "text_input": sanitized_text,
        "text_filtering": "standard",
        "character_voice_gen": voice,
        "narrator_enabled": False,
        "narrator_voice_gen": voice,
        "text_not_inside": "character",
        "language": "en",
        "output_file_name": clean_output_name,
        "output_file_timestamp": False,
        "autoplay": False,
        "autoplay_volume": 0.8
    }
    
    encoded_data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{ALLTALK_BASE_URL}/api/tts-generate",
        data=encoded_data,
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=360) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            elapsed = time.time() - t0
            print(f"   ✅ Audio generated on server in {elapsed:.1f}s!")
            
            # Download file
            remote_url = f"{ALLTALK_BASE_URL}/audio/{clean_output_name}.wav"
            local_path = os.path.join(DEFAULT_OUT_DIR, f"{clean_output_name}.wav")
            print(f"   ⬇️ Downloading audio to {local_path}...")
            urllib.request.urlretrieve(remote_url, local_path)
            file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
            print(f"   🎉 Ready! File saved ({file_size_mb:.2f} MB): {local_path}")
            return local_path
    except Exception as e:
        print(f"   ❌ Generation failed: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFUC AI Studio Voice Generator")
    parser.add_argument("--list-voices", action="store_true", help="List all available cloned voices")
    parser.add_argument("--voice", default="Morgan_Freeman CC3.wav", help="Voice file name from AllTalk")
    parser.add_argument("--text", help="Text script to generate")
    parser.add_argument("--output", default="broadcast_audio", help="Output filename without extension")
    
    args = parser.parse_args()
    if args.list_voices:
        list_voices()
    elif args.text:
        generate_audio(args.text, args.voice, args.output)
    else:
        print("Usage: python generate_ai_audio.py --text \"Your text here\" --voice \"Morgan_Freeman CC3.wav\"")
        print("       python generate_ai_audio.py --list-voices")
