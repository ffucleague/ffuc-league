import os
import sys
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("scripts/broadcast_scripts/week10_script.txt", "r", encoding="utf-8") as f:
    script_text = f.read().strip()

from generate_ai_audio import generate_audio

print("🎙️ Synthesizing Week 10 Audio with AllTalk TTS...")
wav_path = generate_audio(script_text, voice="male_01.wav", output_name="wk10_recap")

if wav_path and os.path.exists(wav_path):
    print(f"✅ Generated WAV: {wav_path}")
    mp3_path = wav_path.replace(".wav", ".mp3")
    remote_wav = "/tmp/wk10_recap.wav"
    remote_mp3 = "/tmp/wk10_recap.mp3"
    
    print("Converting to MP3 via remote ffmpeg...")
    subprocess.run(["scp", wav_path, f"mark@192.168.86.67:{remote_wav}"], check=True)
    subprocess.run(["ssh", "mark@192.168.86.67", f"ffmpeg -y -i {remote_wav} -codec:a libmp3lame -qscale:a 2 {remote_mp3}"], check=True)
    subprocess.run(["scp", f"mark@192.168.86.67:{remote_mp3}", mp3_path], check=True)
    
    if os.path.exists(mp3_path):
        print(f"🎉 Success! Generated MP3 at {mp3_path} ({os.path.getsize(mp3_path)/1024:.1f} KB)")
else:
    print("❌ Failed to generate WAV file")
