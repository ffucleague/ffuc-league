import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_ai_audio import generate_audio

SCRIPT_WK7 = (
    "Welcome to the official Week seven F.F.U.C. broadcast! We have reached the exact halfway mark of the season, and Week seven delivered pure chaos! "
    "Robert roars back from the cellar with a league-best one hundred fifty-three point eight points, led by Tony Pollard's thirty-five point eruption, to claim the High Roller crown! "
    "And in the biggest blowout in modern league history, Robert annihilated Pedro by over one hundred points, crushing him one hundred fifty-three to fifty-two! "
    "Pedro is now firmly stranded in the punishment dungeon with six hundred two season points and zero dollars in FAAB! "
    "Meanwhile, Arnulfo edges Eric by less than three points to capture the ten dollar narrowest victory bounty and seize a share of first place with eye Rob at five and two! "
    "Mark topples eye Rob with a massive one hundred forty-five points, Franky drops one hundred fifty on Alex, and a ferocious five-way logjam forms at three and four! "
    "In pick em, Arnulfo takes solo first place at sixty-seven points. Get ready for Week eight!"
)

print("🎙️ Generating Week 7 Official League Broadcast Audio (Natural Male Voice)...")
local_path = generate_audio(SCRIPT_WK7, voice="male_01.wav", output_name="wk7_recap")

if local_path and os.path.exists(local_path):
    print(f"🎉 Successfully created Week 7 recap audio at: {local_path}")
else:
    print("❌ Audio generation failed!")
