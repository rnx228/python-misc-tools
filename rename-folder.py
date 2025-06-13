import os

def rename_folders(base_path, target_word="folder", dry_run=False):
    target_word = target_word.lower()
    
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)

        if os.path.isdir(folder_path) and target_word in folder_name.lower():
            # Remove target word and clean up the name
            new_name = folder_name.lower().replace(target_word, "").replace("-", "").strip()
            new_name = " ".join(new_name.split())  # Normalize spaces
            new_path = os.path.join(base_path, new_name)

            if new_name and not os.path.exists(new_path):
                print(f'Renaming: "{folder_name}" -> "{new_name}"')
                if not dry_run:
                    os.rename(folder_path, new_path)
            else:
                print(f'Skipping: "{folder_name}" (new name is empty or already exists)')

# === Customize these ===
base_directory = r"C:\Users\"  # 👈 Change this to your folder
word_to_remove = "folder"  # 👈 Change this to any word you want to strip
do_dry_run = False         # 👈 Set to True to preview changes only

rename_folders(base_directory, target_word=word_to_remove, dry_run=do_dry_run)
