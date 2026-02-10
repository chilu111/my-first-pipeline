import os

def process_file(filename):
    try:
        # Atomic open prevents TOCTOU race conditions
        with open(filename, "r", opener=lambda path, flags: os.open(path, flags | os.O_NOFOLLOW)) as f:
            content = f.read()
            return f"Processed: {content}"
    except FileNotFoundError:
        return "File not found"
    except OSError:
        return "Unsafe file access blocked"
