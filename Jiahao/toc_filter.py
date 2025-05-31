def is_valid_toc_line(line: str) -> bool:
    line = line.strip()

    # 1. Must start with a number pattern like 1. or 1.1. or 2.3.5.
    if not re.match(r'^\d+(\.\d+)*\.\s?', line):
        return False

    # 2. Must contain alphabetic characters
    if not re.search(r'[A-Za-zÄÖÜäöüß]', line):
        return False

    # 3. Exclude known keywords unrelated to TOC
    if re.search(r'\b(Revision|Ausgabe|edition|Version)\b', line, re.IGNORECASE):
        return False

    # 4. Too short or mostly numeric
    if len(line) < 5:
        return False
    if re.fullmatch(r'\d+(\.\d+)*', line):
        return False
    if re.fullmatch(r'\d{2}\.\d{2}\.\d{2,4}', line):
        return False

    return True
