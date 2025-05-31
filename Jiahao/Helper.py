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
        

def sort_toc_lines(toc_lines):
    def toc_sort_key(line):
        match = re.match(r"^(\d+(\.\d+)*\.)", line)
        if match:
            return [int(x) for x in match.group(1).strip('.').split('.')]
        return [float('inf')]
    return sorted(toc_lines, key=toc_sort_key)



def separate_on_number(text):
    lines = text.splitlines()
    separated_lines = []

    for line in lines:
        # Look for pattern: a space followed by a number
        match = re.search(r'\s(\d+[\.\d]*)', line)
        if match:
            idx = match.start(1)  # index of the start of the number
            separated_lines.append(line[:idx].strip())
            separated_lines.append(line[idx:].strip())
        else:
            separated_lines.append(line.strip())

    return separated_lines


def is_valid_toc_line(line: str) -> bool:
    line = line.strip()

    # 1. Must start with a number pattern like 1. or 1.1. or 2.3.5.
    if not re.match(r'^\d+(\.\d+)*\.\s?', line):
        return False
    
    # 2. Must contain alphabetic characters
    if not re.search(r'[A-Za-zÄÖÜäöüß]', line):
        return False

    # 3. Exclude known keywords unrelated to TOC
    if re.search(r'\b(Revision|Ausgabe|edition|Version|DOC)\b', line, re.IGNORECASE):
        return False

    if re.match(r'^\d+\.\s?[A-Za-z0-9_]+\.(DOC|PDF|TXT|XLSX?)', line, re.IGNORECASE):
        return False
    
    # 4. Too short or mostly numeric
    if len(line) < 5:
        return False
    if re.fullmatch(r'\d+(\.\d+)*', line):
        return False
    if re.fullmatch(r'\d{2}\.\d{2}\.\d{2,4}', line):
        return False

    return True


def separate_on_number(text):
    lines = text.splitlines()
    separated_lines = []

    for line in lines:
        # Look for pattern: a space followed by a number
        match = re.search(r'\s(\d+[\.\d]*)', line)
        if match:
            idx = match.start(1)  # index of the start of the number
            separated_lines.append(line[:idx].strip())
            separated_lines.append(line[idx:].strip())
        else:
            separated_lines.append(line.strip())

    return separated_lines