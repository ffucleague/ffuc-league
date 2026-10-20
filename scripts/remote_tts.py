import urllib.request, urllib.parse, json, time, os, re

ALLTALK_URL = "http://127.0.0.1:7851"

def gen(text, voice, name):
    print(f"\n[TTS] Generating {name} with voice {voice}...")
    t0 = time.time()
    payload = {
        "text_input": text,
        "text_filtering": "standard",
        "character_voice_gen": voice,
        "narrator_enabled": False,
        "narrator_voice_gen": voice,
        "text_not_inside": "character",
        "language": "en",
        "output_file_name": name,
        "output_file_timestamp": False,
        "autoplay": False,
        "autoplay_volume": 0.8
    }
    encoded = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(f"{ALLTALK_URL}/api/tts-generate", data=encoded, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=300) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"[TTS] Generated in {time.time()-t0:.1f}s. Result: {res.get('status')}")

script_mcafee = (
    "Welcome to the official Week six F.F.U.C. broadcast! What an absolute bloodbath! "
    "Franky and CULT OF THE LAMB explode for one hundred forty-nine point eight points, taking down Joey in a legendary shootout to seize the High Roller crown! "
    "Pedro finally awakens, locking down the ten dollar defense bounty with Kansas City and stomping Alex! "
    "Herrador drops a fifty-point hammer on Arnulfo, while eye Rob claims sole possession of first place at five and one! "
    "And over in the punishment lab, Robert puts up a catastrophic seventy-nine point six, strapping on the sneakers for the five K toilet run! "
    "In pick em, Arnulfo and Robert are locked in a dead heat at fifty-eight points. Let's roll into Week seven!"
)

script_freeman = (
    "Welcome to the official Week six F.F.U.C. broadcast. "
    "In an unforgiving league, fortune favors the bold. Franky and CULT OF THE LAMB rose to the mountaintop with one hundred forty-nine point eight points, defeating Joey in an epic duel. "
    "Pedro found redemption, claiming the ten dollar defense bounty with the Kansas City Chiefs and handing Alex a decisive defeat. "
    "Herrador dismantled Arnulfo, while eye Rob stands alone atop the standings at five and one. "
    "Yet sorrow finds Robert, who collapsed with seventy-nine point six points and now stares down the five K toilet punishment. "
    "In pick em, Arnulfo and Robert share the throne at fifty-eight points. The season marches on."
)

gen(script_mcafee, "pat_mcafee.wav", "wk6_recap_mcafee")
gen(script_freeman, "Morgan_Freeman CC3.wav", "wk6_recap_freeman")
print("\n[TTS] Done with both audio generations!")
