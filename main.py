# main.py

# --- 1. IMPORTS ---
# We are importing pre-built Python packages (libraries) to provide our script with specific "tools".
# Think of this as gathering your toolbox before starting a project.
import os  # The 'os' library lets us interact with the operating system, for tasks like checking if a folder exists, creating folders, and moving files.
import time # The 'time' library gives us time-related functions. We will use it later to pause our script.
from PIL import Image # From the 'Pillow' library (PIL), we import the 'Image' tool, which is essential for opening and reading pixel data from image files.
import pytesseract # This is the Python connector for Tesseract. It acts as a bridge between our script and the Tesseract-OCR engine you installed.
from googletrans import Translator, LANGUAGES # From the 'googletrans' library, we import the 'Translator' tool to perform the translation, and 'LANGUAGES' which is a helpful list of all supported languages.

# --- 2. CONFIGURATION ---
# These are global settings for our script. By keeping them at the top,
# we can easily change how the script behaves without searching through all the code.
FOLDER_TO_WATCH = r'F:\image_translator\images_to_process'
PROCESSED_FOLDER = os.path.join(FOLDER_TO_WATCH, 'processed') # Define the processed folder path once

# TESSERACT EXECUTABLE PATH: The pytesseract library needs to know where the Tesseract program
# is located on your computer. If it's not in a standard system location, we must provide the full path to it.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# --- 3. SETUP FUNCTION ---
def setup_environment():
    """
    This function checks if the required folders exist and creates them if they don't.
    This prevents the script from crashing if a folder is missing.
    """
    if not os.path.exists(FOLDER_TO_WATCH):
        print(f"Creating watch folder: '{FOLDER_TO_WATCH}'")
        os.makedirs(FOLDER_TO_WATCH)
    if not os.path.exists(PROCESSED_FOLDER):
        print(f"Creating processed folder: '{PROCESSED_FOLDER}'")
        os.makedirs(PROCESSED_FOLDER)
    print("-" * 30)
    print("Environment setup complete.")
    print(f"Watching for images in: {FOLDER_TO_WATCH}")
    print("Press Ctrl+C to stop the script.")
    print("-" * 30)

# --- 4. OCR FUNCTION ---
def extract_text_from_image(image_path):
    """
    Takes the file path of an image, opens it, and uses Tesseract to extract text.
    """
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
            return text.strip()
    except pytesseract.TesseractNotFoundError:
        print(f"\nERROR: Tesseract executable not found. Please check the path: '{pytesseract.pytesseract.tesseract_cmd}'")
        return None
    except Exception as e:
        print(f"Could not read image or perform OCR on '{os.path.basename(image_path)}'. Error: {e}")
        return None

# --- 5. TRANSLATION FUNCTION ---
def translate_text_to_english(text):
    """
    Takes a string of text and translates it to English.
    """
    if not text:
        return None
    try:
        translator = Translator()
        translation_result = translator.translate(text, dest='en')
        source_language_name = LANGUAGES.get(translation_result.src, "Unknown")
        return {
            "translated_text": translation_result.text,
            "source_lang_name": source_language_name.capitalize()
        }
    except Exception as e:
        print(f"Translation failed. Could not connect to translation service. Error: {e}")
        return None

# --- 6. CORE PROCESSING FUNCTION ---
def process_files_in_folder():
    """
    Checks for files in the watch folder, processes one file, and then moves it.
    """
    # os.listdir() gets everything in the folder (files and other folders).
    # We use a list comprehension to build a list of only the files.
    # os.path.isfile() returns True if the path is a file.
    try:
        files = [f for f in os.listdir(FOLDER_TO_WATCH) if os.path.isfile(os.path.join(FOLDER_TO_WATCH, f))]
    except FileNotFoundError:
        print(f"ERROR: Watch folder not found at '{FOLDER_TO_WATCH}'. Exiting.")
        return # Exit the function if the folder doesn't exist.

    # If the list of files is empty, there's nothing to do.
    if not files:
        return # Exit the function and wait for the next check.

    # Get the name of the first file in the list.
    filename = files[0]
    image_path = os.path.join(FOLDER_TO_WATCH, filename)
    
    print(f"\n>>> Found new file: '{filename}'")
    
    # --- Step 1: Extract text ---
    original_text = extract_text_from_image(image_path)
    
    # --- Step 2: Translate text (if any was found) ---
    if original_text:
        print(f"\n--- Extracted Text ---\n{original_text}\n----------------------")
        translation_info = translate_text_to_english(original_text)
        if translation_info:
            print(f"Detected Language: {translation_info['source_lang_name']}")
            print(f"\n--- Translated Text (English) ---\n{translation_info['translated_text']}\n---------------------------------")
    else:
        # This 'else' runs if extract_text_from_image returned None or an empty string.
        print("No text could be detected in the image.")

    # --- Step 3: Move the processed file ---
    try:
        destination_path = os.path.join(PROCESSED_FOLDER, filename)
        os.rename(image_path, destination_path)
        print(f"Moved '{filename}' to the 'processed' folder.")
    except Exception as e:
        print(f"ERROR: Could not move file '{filename}'. It may be in use. Error: {e}")


# --- 7. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    setup_environment()
    
    # This 'try...except' block lets us stop the script gracefully.
    try:
        # This is the main loop of our program. 'while True:' means it will run forever.
        while True:
            # Call our processing function.
            process_files_in_folder()
            
            # Tell the script to pause for 5 seconds.
            # This prevents it from checking the folder thousands of times a second, which would waste CPU resources.
            time.sleep(5)
            
    except KeyboardInterrupt:
        # If the user presses Ctrl+C in the terminal, the 'while' loop will be interrupted
        # and this code will run instead of showing an ugly error message.
        print("\nScript stopped by user. Goodbye!")
