import fitz  
from PIL import Image
import pytesseract
import io
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_toc_pages(pdf_path, lang='deu'):
    doc = fitz.open(pdf_path)  # Open PDF file
    toc_pages = {}

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes()))
        text = pytesseract.image_to_string(img, lang=lang)

        if "inhaltsverzeichnis" in text.lower():
            #toc_pages[page_num + 1] = text  # store text with human-friendly page number
            return text