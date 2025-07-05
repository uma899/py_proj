import os
import shutil

def copy_and_rename_files(source_folder, destination_folder):
    """
    Copies files from source_folder to destination_folder,
    removing '_modified' from the filename if present.

    Args:
        source_folder (str): The path to the source directory.
        destination_folder (str): The path to the destination directory.
    """
    # Ensure source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        return

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    print(f"Copying and renaming files from '{source_folder}' to '{destination_folder}'...")

    for filename in os.listdir(source_folder):
        if "_modified" in filename:
            source_path = os.path.join(source_folder, filename)

            # Construct the new filename by removing '_modified'
            new_filename = filename.replace("_modified", "")
            destination_path = os.path.join(destination_folder, new_filename)

            try:
                shutil.copy2(source_path, destination_path)
                print(f"Copied '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error copying '{filename}': {e}")
        else:
            print(f"Skipping '{filename}' as it does not contain '_modified'.")

if __name__ == "__main__":
    # --- Configuration ---
    # IMPORTANT: Replace these with your actual folder paths
    source_directory = "./temp"
    destination_directory = "./renamed"
    # ---------------------

    # Example usage (uncomment and modify paths to run)
    # Create some dummy files for testing if needed
    # os.makedirs(source_directory, exist_ok=True)
    # with open(os.path.join(source_directory, "image_modified.jpg"), "w") as f: f.write("dummy content")
    # with open(os.path.join(source_directory, "document_modified.pdf"), "w") as f: f.write("dummy content")
    # with open(os.path.join(source_directory, "report.docx"), "w") as f: f.write("dummy content")

    copy_and_rename_files(source_directory, destination_directory)

    print("\nCopy and rename process complete.")