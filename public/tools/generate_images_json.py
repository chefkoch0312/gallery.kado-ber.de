import os
import json

IMAGE_FOLDER = "../images"
OUTPUT_FILE = "../data/images.json"

DEFAULT_ALT = "Galeriebild"
DEFAULT_CATEGORY = "AI"
DEFAULT_TAGS = ["robot", "blue", "cyber"]

image_files = sorted([
    f for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

image_data = [{"src": f"/images/{f}", "alt": DEFAULT_ALT, "category": DEFAULT_CATEGORY, "tags": DEFAULT_TAGS} for f in image_files]

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(image_data, out, indent=2, ensure_ascii=False)

print(f"{len(image_data)} Einträge erfolgreich in {OUTPUT_FILE} geschrieben.")
