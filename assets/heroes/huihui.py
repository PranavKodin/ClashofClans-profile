import os

folder_path = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        new_name = filename.replace("_", "")
        if new_name != filename:
            os.rename(
                os.path.join(folder_path, filename),
                os.path.join(folder_path, new_name)
            )
            print(f"Renamed: {filename} → {new_name}")

print("✅ All underscores removed!")
