import os
import subprocess

def format_files_with_black(folder_path):
    """
    Formats all Python files in a given folder using the 'black' formatter.

    Args:
        folder_path (str): The path to the folder containing Python files.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    print(f"Formatting Python files in '{folder_path}' using 'black'...")

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Attempting to format: {file_path}")
                try:
                    # Run black as a subprocess
                    # '--quiet' suppresses verbose output
                    # '--check' can be added if you only want to check for formatting issues
                    # '--diff' can be added to see the diff instead of applying changes
                    result = subprocess.run(['black', file_path], capture_output=True, text=True, check=False)

                    if result.returncode == 0:
                        # Black returns 0 for success, and 1 if files were reformatted
                        # 123 if there was a syntax error or internal error
                        if "reformatted" in result.stdout or "reformatted" in result.stderr:
                             print(f"  Successfully formatted: {file_path}")
                        else:
                             print(f"  No changes needed for: {file_path}")
                    elif result.returncode == 1: # Black exit code 1 means files were reformatted
                        print(f"  Successfully reformatted: {file_path}")
                    else:
                        print(f"  Error formatting {file_path}:")
                        print(f"    Stdout: {result.stdout.strip()}")
                        print(f"    Stderr: {result.stderr.strip()}")

                except FileNotFoundError:
                    print("  Error: 'black' command not found. Please ensure Black is installed and in your PATH.")
                    return
                except Exception as e:
                    print(f"  An unexpected error occurred while formatting {file_path}: {e}")

    print("\nFormatting process complete.")

if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your folder
    target_folder = "./renamed"

    # Example: If your script is in the parent directory of your 'my_python_project'
    # target_folder = os.path.join(os.path.dirname(__file__), 'my_python_project')
    # If your script is inside the folder you want to format, use:
    # target_folder = os.path.dirname(__file__)


    format_files_with_black(target_folder)