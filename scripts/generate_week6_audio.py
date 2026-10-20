import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_ai_audio import generate_audio

SCRIPT_MCAFEE = (
    "Welcome to the official Week six F.F.U.C. broadcast! What an absolute bloodbath! "
    "Franky and CULT OF THE LAMB explode for one hundred forty-nine point eight points, taking down Joey in a legendary shootout to seize the High Roller crown! "
    "Pedro finally awakens, locking down the ten dollar defense bounty with Kansas City and stomping Alex! "
    "Herrador drops a fifty-point hammer on Arnulfo, while eye Rob claims sole possession of first place at five and one! "
    "And over in the punishment lab, Robert puts up a catastrophic seventy-nine point six, strapping on the sneakers for the five K toilet run! "
    "In pick em, Arnulfo and Robert are locked in a dead heat at fifty-eight points. Let's roll into Week seven!"
)

SCRIPT_FREEMAN = (
    "Welcome to the official Week six F.F.U.C. broadcast. "
    "In an unforgiving league, fortune favors the bold. Franky and CULT OF THE LAMB rose to the mountaintop with one hundred forty-nine point eight points, defeating Joey in an epic duel. "
    "Pedro found redemption, claiming the ten dollar defense bounty with the Kansas City Chiefs and handing Alex a decisive defeat. "
    "Herrador dismantled Arnulfo, while eye Rob stands alone atop the standings at five and one. "
    "Yet sorrow finds Robert, who collapsed with seventy-nine point six points and now stares down the five K toilet punishment. "
    "In pick em, Arnulfo and Robert share the throne at fifty-eight points. The season marches on."
)

print("🎙️ Generating Week 6 Pat McAfee audio...")
generate_audio(SCRIPT_MCAFEE, voice="pat_mcafee.wav", output_name="wk6_recap_mcafee")

print("\n🎙️ Generating Week 6 Morgan Freeman audio...")
generate_audio(SCRIPT_FREEMAN, voice="Morgan_Freeman CC3.wav", output_name="wk6_recap_freeman")

print("\n🎉 Both audios generated successfully!")
