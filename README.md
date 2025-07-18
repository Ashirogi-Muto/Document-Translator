# Image Text Translator

This is a Python script that monitors a folder for new image files, extracts any text from them using Tesseract OCR, and then translates that text into English using the Google Translate API.

## Features

* Automatically processes new images dropped into a folder.
* Uses Tesseract for Optical Character Recognition (OCR).
* Translates text from any language supported by Google Translate into English.
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
    *(Note: We will create the `requirements.txt` file in a later step!)*
4.  **Configure the script:**
    * Open `main.py` and update the `FOLDER_TO_WATCH` variable.
    * Ensure the `pytesseract.pytesseract.tesseract_cmd` path points to your Tesseract installation.
5.  **Run the script:**
    ```bash
    python main.py
    ```
6.  Drop any image file containing text into the folder you are watching. The translated text will appear in the terminal.