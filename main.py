# main.py

# --- 1. IMPORTS ---
import os
import time
import fitz  # PyMuPDF library for handling PDFs
from PIL import Image
import pytesseract
from googletrans import Translator, LANGUAGES

# --- 2. CONFIGURATION ---
FOLDER_TO_WATCH = r'F:\image_translator\images_to_process'
PROCESSED_FOLDER = os.path.join(FOLDER_TO_WATCH, 'processed')
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
    print(f"Watching for images, text, and PDF files in: {FOLDER_TO_WATCH}")
    print("Press Ctrl+C to stop the script.")
    print("-" * 30)

def extract_text_from_image(image_path_or_object):
    """
    Takes an image file path or an image object and uses Tesseract to extract text.
    This function is now more flexible to accept image data directly from the PDF function.
    """
    try:
        # The 'image_path_or_object' can be a file path (string) or an Image object.
        text = pytesseract.image_to_string(image_path_or_object)
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        print(f"\nERROR: Tesseract executable not found. Please check the path: '{pytesseract.pytesseract.tesseract_cmd}'")
        return ""
    except Exception as e:
        print(f"Could not perform OCR. Error: {e}")
        return ""

def read_text_from_file(file_path):
    """Opens a plain text file (.txt) and reads its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Could not read text file '{os.path.basename(file_path)}'. Error: {e}")
        return None

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file. It handles both text-based and image-based PDFs.
    """
    try:
        # Open the PDF file
        pdf_document = fitz.open(file_path)
        full_text = []

        # Iterate through each page of the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # First, try to extract text directly. This works for text-based PDFs.
            page_text = page.get_text().strip()
            
            # If direct text extraction yields little or no text, assume it's an image.
            if len(page_text) < 20: # A small threshold to detect image-only pages
                print(f"Page {page_num + 1} seems to be an image. Performing OCR...")
                # Render the page as a high-resolution image
                pix = page.get_pixmap(dpi=300)
                # Convert the pixmap to a Pillow Image object
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                # Use our existing OCR function on the image object
                ocr_text = extract_text_from_image(img)
                full_text.append(ocr_text)
            else:
                full_text.append(page_text)
        
        pdf_document.close()
        # Join the text from all pages into a single string
        return "\n".join(full_text).strip()
        
    except Exception as e:
        print(f"Could not process PDF file '{os.path.basename(file_path)}'. Error: {e}")
        return None

def translate_text_to_english(text):
    """Takes a string of text and translates it to English."""
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
    original_text = None

    print(f"\n>>> Found new file: '{filename}'")

    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
        print("File identified as an image. Performing OCR...")
        original_text = extract_text_from_image(file_path)
    elif file_extension == '.txt':
        print("File identified as a text file. Reading content...")
        original_text = read_text_from_file(file_path)
    elif file_extension == '.pdf':
        print("File identified as a PDF. Extracting text...")
        original_text = extract_text_from_pdf(file_path)
    else:
        print(f"Unsupported file type: '{file_extension}'. This file will be moved without processing.")

    if original_text:
        print(f"\n--- Original Text ---\n{original_text}\n---------------------")
        translation_info = translate_text_to_english(original_text)
        if translation_info:
            print(f"Detected Language: {translation_info['source_lang_name']}")
            print(f"\n--- Translated Text (English) ---\n{translation_info['translated_text']}\n---------------------------------")
    else:
        print("No text was extracted from the file.")

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
        while True:
            process_files_in_folder()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nScript stopped by user. Goodbye!")