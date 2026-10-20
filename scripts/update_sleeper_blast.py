import os, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

blast_text = """🚨 F.F.U.C. WEEK 6 OFFICIAL REPORT IS LIVE! 🚨

👑 High Roller ($10 Bounty): CULT OF THE LAMB (Franky) — 149.80 PTS
⚡ $10 DEF Bounty Winner: Pedro & Kansas City Chiefs DEF — 16.00 PTS (upset Alex 112-87!)
💔 Heartbreak of the Week: Joey (135.28 PTS) falls to Franky in a 285-pt shootout
🚽 Toilet Nominee (Week-Low): Defending Champ Robert (79.62 PTS)
👑 Sole Monarch: iRob stands alone at 5-1 atop the mountain!
🎯 Pick-Em Co-Leaders: Arnulfo & Robert tied at 58.0 PTS (95 games)
💵 Next Up (Week 7 Bounty): Narrowest Margin of Victory ($10)

🎙️ AI Broadcasts: Pat McAfee & Morgan Freeman Voice Recaps
🎬 LivePortrait Videos: Franky Coronation & Pedro Forrest Gump 5K Meter
📊 Updated Standings, Power Rankings, All-Play Luck Index & FAAB Ledger:
👉 https://ffucleague.com"""

announcement_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "latest_sleeper_announcement.txt")

with open(announcement_path, "w", encoding="utf-8") as f:
    f.write(blast_text)

print(f"Saved cleanly to {announcement_path}")
print("--- PREVIEW ---")
print(blast_text)
print("---------------")

# Copy to clipboard via powershell
try:
    ps_cmd = f'[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-Content -Path "{announcement_path}" -Raw -Encoding UTF8 | Set-Clipboard'
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    print("✅ Successfully copied to Windows clipboard! (Press Ctrl+V in Sleeper chat)")
except Exception as e:
    print(f"Notice copying to clipboard: {e}")
