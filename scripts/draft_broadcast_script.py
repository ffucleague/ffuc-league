"""
FFUC Broadcast Script Generator powered by Qwen3-VL (32B)
Automates drafting authentic, high-energy sports radio league recaps for Week 7 and all future weeks.
"""

import os
import sys
import json
import time
import re
import argparse
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
OUTPUT_DIR = os.path.join(SCRIPTS_DIR, "broadcast_scripts")
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

config = load_config()
ai_endpoints = config.get("ai_endpoints", {})
DEFAULT_OLLAMA_URL = ai_endpoints.get("ollama_url", "http://192.168.86.67:11434")
DEFAULT_MODEL = ai_endpoints.get("default_broadcast_model", "qwen3-vl:32b")
DEFAULT_VOICE = ai_endpoints.get("default_broadcast_voice", "male_01.wav")
LEAGUE_ID = config.get("league_id", "1389724575532613632")

def sanitize_for_tts(text):
    """
    Cleans and formats text specifically for AllTalk XTTSv2 speech synthesis:
    - Removes markdown syntax (*, #, _, `, [ ])
    - Expands currency ($10 -> ten dollar)
    - Expands numbers and decimals into phonetic words
    - Normalizes acronyms (FFUC -> F.F.U.C., iRob -> eye Rob)
    - Paces sentences with natural pause punctuation
    """
    t = text
    # Strip markdown bold, italic, headers, bullets
    t = re.sub(r'[*_#`\[\]]', '', t)
    t = re.sub(r'^\s*[-•]\s*', '', t, flags=re.MULTILINE)
    
    # Pronunciation mappings
    t = re.sub(r'\bFFUC\b', 'F.F.U.C.', t)
    t = re.sub(r'\biRob\b|\bIrob\b|\bIROB\b', 'eye Rob', t)
    t = re.sub(r'\bPick-Em\b|\bPick-em\b|\bpickem\b', 'pick em', t, flags=re.IGNORECASE)
    t = re.sub(r'\b5K\b', 'five K', t, flags=re.IGNORECASE)
    t = re.sub(r'\bFAAB\b', 'fab', t, flags=re.IGNORECASE)
    t = re.sub(r'\bDEF\b', 'defense', t)
    t = re.sub(r'\bPTS\b|\bpts\b', 'points', t)
    t = re.sub(r'\bTD\b|\bTDs\b', 'touchdowns', t)
    
    # Currency
    t = re.sub(r'\$([0-9]+)', r'\1 dollar', t)
    
    # Number to words dictionary for common sports stats
    num_words = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
        '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
        '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen',
        '18': 'eighteen', '19': 'nineteen', '20': 'twenty', '30': 'thirty',
        '40': 'forty', '50': 'fifty', '60': 'sixty', '70': 'seventy',
        '80': 'eighty', '90': 'ninety', '100': 'one hundred'
    }
    
    # Expand Week numbers
    t = re.sub(r'\bWeek\s*([0-9]+)\b', lambda m: f"Week {num_words.get(m.group(1), m.group(1))}", t, flags=re.IGNORECASE)
    
    # Remove awkward question marks or multiple punctuation
    t = t.replace('?', ',')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n+', ' ', t).strip()
    return t

def load_week_summary(week_num):
    """Extracts high-level story data from weekly JSON if available"""
    data_path = os.path.join(SCRIPTS_DIR, f"week{week_num}_data.json")
    if not os.path.exists(data_path):
        return None
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        summary = {
            "week": week_num,
            "matchups": [],
            "high_roller": None,
            "blowout": None,
            "closest": None,
            "rosters": {}
        }
        
        # High roller
        all_scores = data.get("all_scores", [])
        if all_scores:
            all_scores.sort(key=lambda x: x.get("points", 0), reverse=True)
            summary["high_roller"] = all_scores[0]
            
        # Matchups
        matchup_results = data.get("matchup_results", [])
        if matchup_results:
            # Sort by margin
            sorted_by_margin = sorted(matchup_results, key=lambda x: x.get("margin", 0))
            summary["closest"] = sorted_by_margin[0]
            summary["blowout"] = sorted_by_margin[-1]
            
            for m in matchup_results:
                w = m.get("winner", {})
                l = m.get("loser", {})
                summary["matchups"].append({
                    "winner": w.get("manager_name"),
                    "winner_score": w.get("points"),
                    "loser": l.get("manager_name"),
                    "loser_score": l.get("points"),
                    "margin": round(m.get("margin", 0), 2)
                })
        return summary
    except Exception as e:
        print(f"⚠️ Error parsing week data: {e}")
        return None

def build_prompt(week_num, summary_data=None, custom_notes=None):
    """Constructs prompt for Qwen3-VL to draft a sports broadcast script"""
    
    # Hardcoded or dynamic context for Week 7
    if week_num == 7:
        context = (
            "FFUC Fantasy Football League - Week 7 Highlights:\n"
            "- Exact halfway mark of the season.\n"
            "- High Roller Champion: Robert exploded with 153.82 points (led by Tony Pollard's 35.0-point performance), escaping the cellar.\n"
            "- Century Blowout: Robert annihilated Pedro 153.82 to 52.32! Pedro lost by over 100 points (101.5 pt margin) and is stuck in last place with 0 FAAB.\n"
            "- Bounty Thriller ($10 Narrowest Margin): Arnulfo edged Eric 112.28 to 109.30 (margin 2.98 points) to win the $10 cash bounty and take a share of 1st place.\n"
            "- Heartbreak Loss: Alex put up 129.54 points (4th highest in the league) but ran into Franky's 150.02 blitz.\n"
            "- Shootouts & Standings: Mark beat iRob 145.2 to 104.1. Five teams are now tied at 3-4.\n"
            "- Pick'em: Arnulfo leads solo with 67 points."
        )
    elif summary_data:
        m_lines = "\n".join([f"- {m['winner']} ({m['winner_score']}) defeated {m['loser']} ({m['loser_score']}) by {m['margin']} pts" for m in summary_data.get("matchups", [])])
        hr = summary_data.get("high_roller", {})
        bo = summary_data.get("blowout", {})
        cl = summary_data.get("closest", {})
        context = (
            f"FFUC Fantasy Football League - Week {week_num} Highlights:\n"
            f"- High Roller: {hr.get('manager_name')} with {hr.get('points')} points\n"
            f"- Biggest Blowout: {bo.get('winner', {}).get('manager_name')} ({bo.get('winner', {}).get('points')}) beat {bo.get('loser', {}).get('manager_name')} ({bo.get('loser', {}).get('points')}) by {round(bo.get('margin', 0), 2)} pts\n"
            f"- Closest Matchup: {cl.get('winner', {}).get('manager_name')} ({cl.get('winner', {}).get('points')}) beat {cl.get('loser', {}).get('manager_name')} ({cl.get('loser', {}).get('points')}) by {round(cl.get('margin', 0), 2)} pts\n"
            f"Matchup Results:\n{m_lines}"
        )
    else:
        context = f"FFUC Fantasy Football League - Week {week_num} Recap."

    if custom_notes:
        context += f"\nSpecial Commissioner Notes: {custom_notes}"

    prompt = (
        f"You are the lead sports radio broadcast anchor for the FFUC (Fantasy Football Ultimate Championship). "
        f"Draft a punchy, energetic, 45-to-60 second weekly league recap script based on the following highlights:\n\n"
        f"{context}\n\n"
        f"STRICT RULES FOR BROADCAST SCRIPT:\n"
        f"1. Voice & Tone: Authentic, energetic male sports anchor delivery (think ESPN Radio / local sports anchor). NO celebrity impersonations (no Morgan Freeman, no Pat McAfee).\n"
        f"2. Mandatory Stories: You MUST mention Robert's high score of 153.8 points, Pedro losing by over 100 points, Arnulfo's $10 narrow victory bounty, and Franky's 150-point explosion.\n"
        f"3. Spoken Phonetic Formatting: Write out numbers phonetically (e.g. 'one hundred fifty-three point eight points', 'one hundred points', 'ten dollar bounty', 'Week seven') so it sounds natural in text-to-speech.\n"
        f"4. Pronunciation: Pronounce iRob as 'eye Rob', FFUC as 'F.F.U.C.', and FAAB as 'fab'.\n"
        f"5. NO Markdown: Do not use asterisks, bold tags, bullet points, or headers. Output ONLY the raw spoken radio script as a continuous paragraph."
    )
    return prompt

def generate_script(week_num=7, model=DEFAULT_MODEL, ollama_url=DEFAULT_OLLAMA_URL, custom_notes=None):
    """Queries Qwen3 via Ollama to generate the script"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary_data = load_week_summary(week_num)
    prompt = build_prompt(week_num, summary_data, custom_notes)
    
    print(f"\n=======================================================")
    print(f"🎙️ DRAFTING FFUC WEEK {week_num} BROADCAST SCRIPT WITH QWEN3")
    print(f"   Model: {model}")
    print(f"   Endpoint: {ollama_url}")
    print(f"=======================================================\n")
    print("⏳ Sending request to Qwen3-VL 32B... (streaming response)\n")
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.7,
            "num_predict": 1200
        }
    }
    
    req = urllib.request.Request(
        f"{ollama_url}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    full_response = ""
    has_started_response = False
    sys.stdout.write("🧠 Qwen3 Reasoning ")
    sys.stdout.flush()
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            for line in resp:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    thinking = chunk.get("thinking", "")
                    if thinking and not has_started_response:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                    text = chunk.get("response", "")
                    if text:
                        if not has_started_response:
                            has_started_response = True
                            sys.stdout.write("\n\n=== 🎙️ QWEN3 BROADCAST SCRIPT ===\n")
                            sys.stdout.flush()
                        sys.stdout.write(text)
                        sys.stdout.flush()
                        full_response += text
                    if chunk.get("done", False):
                        break
        elapsed = time.time() - t0
        print(f"\n\n⏱️ Script generated by Qwen3 in {elapsed:.1f}s!")
    except Exception as e:
        print(f"\n❌ Ollama generation error: {e}")
        return None
        
    sanitized = sanitize_for_tts(full_response)
    out_file = os.path.join(OUTPUT_DIR, f"week{week_num}_script.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(sanitized)
        
    print(f"💾 Saved sanitized script to: {out_file}")
    print(f"\n--- SANITIZED FOR ALLTALK TTS ---\n\"{sanitized}\"\n---------------------------------")
    return sanitized

def synthesize_audio(script_text, week_num, voice=DEFAULT_VOICE):
    """Calls generate_ai_audio to produce the final MP3 broadcast"""
    print(f"\n🎙️ Synthesizing Spoken Audio with AllTalk TTS (Voice: {voice})...")
    from generate_ai_audio import generate_audio
    output_name = f"wk{week_num}_recap"
    local_wav = generate_audio(script_text, voice=voice, output_name=output_name)
    if local_wav and os.path.exists(local_wav):
        print(f"✅ WAV generated at {local_wav}")
        # Convert to MP3
        mp3_path = local_wav.replace(".wav", ".mp3")
        os.system(f'ffmpeg -y -i "{local_wav}" -codec:a libmp3lame -qscale:a 2 "{mp3_path}" >nul 2>&1')
        if os.path.exists(mp3_path):
            print(f"🎉 Created broadcast MP3 at {mp3_path}")
            return mp3_path
        return local_wav
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFUC AI Broadcast Script Generator")
    parser.add_argument("--week", type=int, default=7, help="NFL Week number (default: 7)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--notes", help="Special commissioner notes to include in script")
    parser.add_argument("--generate-audio", action="store_true", help="Synthesize spoken audio via AllTalk after drafting script")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"AllTalk voice (default: {DEFAULT_VOICE})")
    
    args = parser.parse_args()
    script = generate_script(args.week, args.model, DEFAULT_OLLAMA_URL, args.notes)
    
    if script and args.generate_audio:
        synthesize_audio(script, args.week, args.voice)
