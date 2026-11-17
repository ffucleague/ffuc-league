import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
BUILD_PATH = os.path.join(BASE_DIR, "scripts", "build_fixed_deck10.py")

pattern = r'[ \t]*<div class="[^"]*absolute top-2 left-2 z-10[^"]*">[\s\S]*?</div>\r?\n?'

for path, name in [(INDEX_PATH, "index.html"), (BUILD_PATH, "build_fixed_deck10.py")]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = list(re.finditer(pattern, content))
        if matches:
            new_content = re.sub(pattern, "", content)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Removed {len(matches)} banners from {name}")
        else:
            print(f"No banners found in {name}")
