[![Python Linter](https://github.com/Ashirogi-Muto/ImageTranslator/actions/workflows/linter.yml/badge.svg)](https://github.com/Ashirogi-Muto/ImageTranslator/actions/workflows/linter.yml)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Document Text Translator

This is a Python script that monitors a folder for new image files, extracts any text from them using Tesseract OCR, and then translates that text into English using the Google Translate API.

## Features

* Automatically processes new files dropped into a folder.
* Handles multiple file types:
    * **Images (`.png`, `.jpg`, etc.):** Extracts text using Tesseract OCR.
    * **Text Files (`.txt`):** Reads text content directly.
    * **PDFs (`.pdf`):** Extracts text from both text-based and scanned (image-based) PDFs.
    * **Word Documents (`.docx`):** Extracts text from Microsoft Word files.
    * **PowerPoint Presentations (`.pptx`):** Extracts text from Microsoft PowerPoint files.
* Translates extracted text from any language into English.
* Moves processed files to a separate subfolder to avoid reprocessing.

## How to Use

1.  **Prerequisites:**
    * Python 3
    * Tesseract-OCR engine installed on your system.
2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Ashirogi-Muto/ImageTranslator.git](https://github.com/Ashirogi-Muto/ImageTranslator.git)
    cd ImageTranslator
    ```
3.  **Install Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure the script:**
    * Open `main.py` and update the `FOLDER_TO_WATCH` variable.
    * Ensure the `pytesseract.pytesseract.tesseract_cmd` path points to your Tesseract installation.
5.  **Run the script:**
    ```bash
    python main.py
    ```
6.  Drop any image file containing text into the folder you are watching. The translated text will appear in the terminal.
