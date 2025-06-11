import os
import shutil

# Set the allowed extensions
TARGET_EXTENSIONS = {'.mp4', '.mkv'}  # Add more if needed

def move_selected_files_to_root(root_folder, extensions):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Skip the root folder itself
        if dirpath == root_folder:
            continue

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in extensions:
                continue  # Skip files not matching the target extensions

            source_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(root_folder, filename)

            # Rename if a file with the same name already exists
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    new_filename = f"{base}_{counter}{ext}"
                    dest_path = os.path.join(root_folder, new_filename)
                    counter += 1

            print(f"Moving: {source_path} -> {dest_path}")
            shutil.move(source_path, dest_path)

    print("Selected files moved to root folder.")

if __name__ == "__main__":
    # Get the directory where the script is located
    main_folder = os.path.dirname(os.path.abspath(__file__))
    move_selected_files_to_root(main_folder, TARGET_EXTENSIONS)
