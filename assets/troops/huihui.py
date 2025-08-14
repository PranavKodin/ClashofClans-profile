import os

folder_path = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder_path):
    # Allowed image types
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        
        # Remove underscores & lowercase
        name_no_underscores = filename.replace("_", "").lower()
        
        # Change extension to .png
        base_name = os.path.splitext(name_no_underscores)[0]
        new_name = f"{base_name}.png"
        
        # Rename if different
        if new_name != filename:
            os.rename(
                os.path.join(folder_path, filename),
                os.path.join(folder_path, new_name)
            )
            print(f"Renamed: {filename} → {new_name}")

print("✅ Done! All files renamed, underscores removed, lowercase applied, and converted to .png.")
