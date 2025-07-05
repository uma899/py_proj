#API_KEY = "AIzaSyBJ66evkNSCrSa_z5s3dCo_H3Yv5Tw9hiE" # Make sure to replace this
import google.generativeai as genai
import os
import filecmp # To compare files

# --- Configuration ---
# IMPORTANT: Replace with your actual Gemini API key
# Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey
API_KEY = "AIzaSyBJ66evkNSCrSa_z5s3dCo_H3Yv5Tw9hiE"# Make sure to replace this

# Input and Output Directories
INPUT_PHP_DIR = './PHPFILES'  # Directory containing your PHP 5.5 files
OUTPUT_PHP_DIR = './updated'  # Directory to save Gemini's suggested files
output_file_path = './updated'  # Directory to save Gemini's suggested files

# Prompt for Gemini
GEMINI_PROMPT = "Modify the following PHP code to be compatible with and leverage features of PHP 8+ (e.g., replace mysql_* with mysqli or PDO, update deprecated deprecated syntax, improve security, use modern PHP features). Keep the HTML structure intact and only modify the PHP parts. Provide only the modified PHP and HTML, no explanations outside the code block."

# --- Setup Gemini API ---
genai.configure(api_key=API_KEY)

# *** CHANGE MADE HERE ***
# Using 'models/gemini-1.0-pro' as it's listed as available in your screenshot.
# You could also try 'models/gemini-1.5-flash' if you prefer a faster model.
model = genai.GenerativeModel('models/gemini-2.0-flash')

# --- Helper Functions ---
def get_gemini_response(file_content, prompt):
    """Sends the file content to Gemini API with the given prompt and returns the response."""
    try:
        response = model.generate_content(f"{prompt}\n\n```php\n{file_content}\n```")
        # Accessing the text from the candidates
        if response.candidates:
            # Join multiple parts if they exist, or just take the first part's text
            return "".join(part.text for part in response.candidates[0].content.parts)
        return None
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return None

def extract_php_code_block(gemini_text):
    """
    Extracts content from the first PHP code block (```php ... ```) in Gemini's response.
    If no such block is found, returns the entire text.
    """
    start_tag = "```php"
    end_tag = "```"

    start_index = gemini_text.find(start_tag)
    if start_index == -1:
        # If no ```php``` block, assume the whole text is the code
        return gemini_text.strip()

    start_index += len(start_tag)
    end_index = gemini_text.find(end_tag, start_index)

    if end_index == -1:
        # If no closing tag, return from start_tag to end
        return gemini_text[start_index:].strip()

    return gemini_text[start_index:end_index].strip()

def process_php_files(input_dir, output_dir, prompt):
    """
    Iterates through PHP files in the input directory, sends them to Gemini,
    and saves the modified code to the output directory with appropriate naming.
    """
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory '{output_dir}' ensured.")

    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.php'):
                input_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(input_file_path, input_dir)
                
                # Create a temporary path for Gemini's suggestion to compare
                temp_output_file_path = os.path.join(output_dir, "temp_" + relative_path)
                os.makedirs(os.path.dirname(temp_output_file_path), exist_ok=True)

                print(f"\nProcessing: {input_file_path}")
                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        original_code = f.read()

                    gemini_response_text = get_gemini_response(original_code, prompt)

                    if gemini_response_text:
                        modified_code = extract_php_code_block(gemini_response_text)

                        # Save to a temporary file for comparison
                        with open(temp_output_file_path, 'w', encoding='utf-8') as f:
                            f.write(modified_code)

                        # Compare original and modified content
                        with open(input_file_path, 'r', encoding='utf-8') as f_orig:
                            orig_content_normalized = f_orig.read().replace('\r\n', '\n').strip()
                        with open(temp_output_file_path, 'r', encoding='utf-8') as f_temp:
                            temp_content_normalized = f_temp.read().replace('\r\n', '\n').strip()

                        base_name, ext = os.path.splitext(file_name)
                        if orig_content_normalized == temp_content_normalized:
                            final_file_name = f"{base_name}_same{ext}"
                            print(f"No significant modifications suggested by Gemini for {file_name}.")
                        else:
                            final_file_name = f"{base_name}_modified{ext}"
                            print(f"Modifications suggested by Gemini for {file_name}.")

                        final_output_file_path = os.path.join(os.path.dirname(output_file_path), final_file_name)
                        
                        # Rename the temporary file to its final name
                        os.rename(temp_output_file_path, final_output_file_path)
                        print(f"Output saved to: {final_output_file_path}")
                        print("-" * 50)
                        print("Remember to review this file carefully for correctness and security!")
                        print("-" * 50)

                    else:
                        print(f"Failed to get a valid response for {file_name}. Skipping.")
                        # Clean up temp file if response failed
                        if os.path.exists(temp_output_file_path):
                            os.remove(temp_output_file_path)

                except Exception as e:
                    print(f"Failed to process {file_name}: {e}")
                    # Ensure temp file is cleaned up on error
                    if os.path.exists(temp_output_file_path):
                        os.remove(temp_output_file_path)

# --- Main Execution ---
if __name__ == "__main__":
        print("Starting PHP code suggestion process using Gemini API...")
        process_php_files(INPUT_PHP_DIR, OUTPUT_PHP_DIR, GEMINI_PROMPT)
        print("\n--- Process Completed ---")
        print("Please review the files in the 'php8_suggested_files' directory carefully.")
        print("AI-generated code is not guaranteed to be perfect or secure without human review.")