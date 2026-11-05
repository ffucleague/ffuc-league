import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meme_engine import add_template, list_templates

CANDIDATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch", "candidate_clips")

templates_to_add = [
    # High Roller
    {
        "file": os.path.join(CANDIDATES_DIR, "shaq_shimmy.mp4"),
        "category": "high_roller",
        "id": "shaq_shimmy",
        "title": "Shaq Shimmy Celebration",
        "character": "Shaquille O'Neal",
        "vibe": "Smug shoulder shimmy victory bounce with big grin"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "wolf_chest_thump.mp4"),
        "category": "high_roller",
        "id": "wolf_chest_thump",
        "title": "Wolf of Wall Street Chest Thump",
        "character": "Mark Hanna (Matthew McConaughey)",
        "vibe": "Wall street chest-thumping rhythm, humming, high roller intensity"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "paid_off_screaming.mp4"),
        "category": "high_roller",
        "id": "paid_off_cash",
        "title": "Paid Off Cash Celebration",
        "character": "Michael Torpey (Paid Off)",
        "vibe": "High-energy game show host screaming and flaunting cold hard cash"
    },
    
    # Heartbreak
    {
        "file": os.path.join(CANDIDATES_DIR, "michael_scott_heartbreak.mp4"),
        "category": "heartbreak",
        "id": "michael_scott_heartbreak",
        "title": "Michael Scott Holding Back Tears",
        "character": "Michael Scott (Steve Carell)",
        "vibe": "Grimacing, biting lip, nodding and holding back painful tears"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "homelander_stress.mp4"),
        "category": "heartbreak",
        "id": "homelander_stress",
        "title": "Homelander Psychotic Stare",
        "character": "Homelander (Antony Starr)",
        "vibe": "Suppressed rage, twitching eye, internal devastation and panic"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "dazn_waiting.mp4"),
        "category": "heartbreak",
        "id": "dazn_waiting",
        "title": "Sad Stadium Fan Waiting",
        "character": "Sad Fan",
        "vibe": "Slumped over in stadium seats, lonely depression after a brutal defeat"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "spiderman_crying.mp4"),
        "category": "heartbreak",
        "id": "spiderman_crying",
        "title": "Spider-Man Peter Parker Crying",
        "character": "Peter Parker (Tobey Maguire)",
        "vibe": "Iconic sobbing grimace, tear rolling down, utter heartbreak"
    },
    
    # Toilet Runner
    {
        "file": os.path.join(CANDIDATES_DIR, "frankie_lapenna_run.mp4"),
        "category": "toilet_runner",
        "id": "frankie_lapenna_run",
        "title": "Frankie LaPenna Power Sprint",
        "character": "Frankie LaPenna",
        "vibe": "High-speed frantic running with huge dump truck hips fleeing last place"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "panic_run_away.mp4"),
        "category": "toilet_runner",
        "id": "forrest_field_sprint",
        "title": "Forrest Gump Football Field Sprint",
        "character": "Forrest Gump (Tom Hanks)",
        "vibe": "Endless sprint across the gridiron out of the stadium in full panic"
    },
    {
        "file": os.path.join(CANDIDATES_DIR, "empty_wallet_broke.mp4"),
        "category": "toilet_runner",
        "id": "empty_wallet_broke",
        "title": "Empty Wallet Broke Panic",
        "character": "Struggling Manager",
        "vibe": "Staring inside empty wallet with utter despair and financial ruin"
    }
]

print("=== Registering and Syncing Approved Templates to Catalog & FaceFusion Container ===\n")
for t in templates_to_add:
    print(f"Adding [{t['category'].upper()}] -> '{t['id']}' ({t['title']})...")
    add_template(
        file_path=t["file"],
        category=t["category"],
        template_id=t["id"],
        title=t["title"],
        character=t["character"],
        vibe=t["vibe"]
    )
    print("-" * 50)

print("\n🎉 All approved templates registered and synced successfully!\n")
list_templates()
