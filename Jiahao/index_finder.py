def extract_toc_pages(pdf_path, lang='deu'):
    doc = fitz.open(pdf_path)  # Open PDF file
    toc_pages = {}

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes()))
        text = pytesseract.image_to_string(img, lang=lang)

        if "inhaltsverzeichnis" in text.lower():
            print(f"--- Page {page_num + 1} contains 'Inhaltsverzeichnis' ---")
            print(text)
            print("\n")
            toc_pages[page_num + 1] = text  # store text with human-friendly page number

    return toc_pages