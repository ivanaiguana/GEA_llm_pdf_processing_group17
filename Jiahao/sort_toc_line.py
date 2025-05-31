def sort_toc_lines(toc_lines):
    def toc_sort_key(line):
        match = re.match(r"^(\d+(\.\d+)*\.)", line)
        if match:
            return [int(x) for x in match.group(1).strip('.').split('.')]
        return [float('inf')]
    return sorted(toc_lines, key=toc_sort_key)