def filter_blast_reference(text):
    """
    Remove the Reference section from BLAST output, and remove the empty line before Reference
    """
    lines = text.splitlines()
    filtered = []
    skip = False
    for line in lines:
        # Detect the start of Reference section
        if line.strip().startswith("Reference"):
            # If the previous line is empty, remove it
            if filtered and filtered[-1].strip() == "":
                filtered.pop()
            skip = True
        # Skip Reference section
        if skip:
            # Reference section ends with an empty line
            if line.strip() == "":
                skip = False
            continue
        filtered.append(line)
    return "\n".join(filtered) 