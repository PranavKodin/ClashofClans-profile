import os
import re

folder_path = os.path.dirname(os.path.abspath(__file__))  # Same folder as script

for filename in os.listdir(folder_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        # Remove extension for processing
        name, _ = os.path.splitext(filename)

        # Remove underscores, "info", "spell" (case-insensitive)
        clean_name = re.sub(r'[_\s]+', '', name)  # Remove underscores and extra spaces
        clean_name = re.sub(r'info', '', clean_name, flags=re.IGNORECASE)
        clean_name = re.sub(r'spell', '', clean_name, flags=re.IGNORECASE)

        # Final filename: lowercase + .png
        new_name = clean_name.lower() + ".png"

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")

print("✅ Done renaming files!")
