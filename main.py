# main.py

# --- 1. IMPORTS ---
import os  # Provides tools to interact with the operating system, like managing files and folders.
import time  # Provides time-related functions, used here to pause the script.
from PIL import Image  # From the Pillow library, used for opening and processing image files.
import pytesseract  # The Python interface for the Tesseract-OCR engine.
from googletrans import Translator, LANGUAGES  # From the googletrans library, used for translation.

# --- 2. CONFIGURATION ---
# The full path to the folder that the script will monitor for new files.
FOLDER_TO_WATCH = r'F:\image_translator\images_to_process'
# The full path to the subfolder where processed files will be moved.
PROCESSED_FOLDER = os.path.join(FOLDER_TO_WATCH, 'processed')
# The full path to the Tesseract executable file. This is required on Windows.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- 3. HELPER FUNCTIONS ---

def setup_environment():
    """Checks if the required folders exist and creates them if they don't."""
    if not os.path.exists(FOLDER_TO_WATCH):
        print(f"Creating watch folder: '{FOLDER_TO_WATCH}'")
        os.makedirs(FOLDER_TO_WATCH)
    if not os.path.exists(PROCESSED_FOLDER):
        print(f"Creating processed folder: '{PROCESSED_FOLDER}'")
        os.makedirs(PROCESSED_FOLDER)
    print("-" * 30)
    print("Environment setup complete.")
    print(f"Watching for images and text files in: {FOLDER_TO_WATCH}")
    print("Press Ctrl+C to stop the script.")
    print("-" * 30)

def extract_text_from_image(image_path):
    """Takes an image file path and uses Tesseract to extract text."""
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

def read_text_from_file(file_path):
    """
    Opens a plain text file (.txt) and reads its entire content into a single string.
    The 'encoding="utf-8"' parameter is crucial for correctly handling special characters
    and text from a wide variety of languages.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Could not read text file '{os.path.basename(file_path)}'. Error: {e}")
        return None

def translate_text_to_english(text):
    """Takes a string of text and translates it to English using the googletrans library."""
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

# --- 4. CORE PROCESSING FUNCTION ---
def process_files_in_folder():
    """Checks for files, processes one based on its type, and then moves it."""
    try:
        files = [f for f in os.listdir(FOLDER_TO_WATCH) if os.path.isfile(os.path.join(FOLDER_TO_WATCH, f))]
    except FileNotFoundError:
        print(f"ERROR: Watch folder not found at '{FOLDER_TO_WATCH}'. Exiting.")
        return

    if not files:
        return

    filename = files[0]
    file_path = os.path.join(FOLDER_TO_WATCH, filename)
    original_text = None  # Initialize a variable to hold the extracted text.

    print(f"\n>>> Found new file: '{filename}'")

    # This block determines how to process the file based on its extension.
    # os.path.splitext() splits "file.txt" into ("file", ".txt").
    # We get the extension at index [1] and convert it to lowercase for reliable comparison.
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
        print("File identified as an image. Performing OCR...")
        original_text = extract_text_from_image(file_path)
    elif file_extension == '.txt':
        print("File identified as a text file. Reading content...")
        original_text = read_text_from_file(file_path)
    else:
        # If the file extension is not in our supported lists, we skip processing.
        print(f"Unsupported file type: '{file_extension}'. This file will be moved without processing.")

    # This block handles the translation and printing of results.
    # It only runs if the 'original_text' variable successfully received content.
    if original_text:
        print(f"\n--- Original Text ---\n{original_text}\n---------------------")
        translation_info = translate_text_to_english(original_text)
        if translation_info:
            print(f"Detected Language: {translation_info['source_lang_name']}")
            print(f"\n--- Translated Text (English) ---\n{translation_info['translated_text']}\n---------------------------------")
    else:
        # This message appears if no text was extracted, or the file type was unsupported.
        print("No text was extracted from the file.")

    # This block moves the file to the 'processed' folder after attempting to process it.
    try:
        destination_path = os.path.join(PROCESSED_FOLDER, filename)
        os.rename(file_path, destination_path)
        print(f"Moved '{filename}' to the 'processed' folder.")
    except Exception as e:
        print(f"ERROR: Could not move file '{filename}'. It may be in use. Error: {e}")

# --- 5. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    setup_environment()
    try:
        # This 'while True' loop makes the script run continuously.
        while True:
            process_files_in_folder()
            # The script pauses for 5 seconds before checking the folder again.
            time.sleep(5)
    except KeyboardInterrupt:
        # This allows the user to stop the script cleanly by pressing Ctrl+C.
        print("\nScript stopped by user. Goodbye!")
