import os

folder_path = os.path.dirname(os.path.abspath(__file__))  # Same folder as script

for filename in os.listdir(folder_path):
    if filename.lower().endswith("_info.webp"):
        clean_name = filename.strip()  # Remove extra spaces
        clean_name = clean_name.replace("_", "")  # Remove all underscores
        new_name = clean_name[:-10] + ".png"  # Remove `_info.webp` and add `.png`
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name.lower())  # Lowercase
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name.lower()}")

print("✅ Done renaming files!")
