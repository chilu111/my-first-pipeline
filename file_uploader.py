import re
import os

# Allow only a minimal set of safe file types (tight allowlist = smaller attack surface).
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def is_allowed_extension(filename: str) -> bool:
    """
    Accept files only if they have an extension and it's in ALLOWED_EXTENSIONS.
    Blocks scripts/executables like .php, .exe, .js, .sh, etc.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_secure(file):
    """
    Secure upload flow:
      1) Sanitize the user-provided name (neutralize traversal / odd chars).
      2) Enforce extension allowlist (reject dangerous types).
      3) Save into a dedicated uploads directory via safe path join.
    """
    raw_name = getattr(file, "filename", "")
    safe_name = secure_filename(raw_name)  # e.g., "../../../etc/passwd" -> "etc_passwd"

    if not safe_name:
        return "Error: Invalid or empty filename."

    if not is_allowed_extension(safe_name):
        return "Error: File type not allowed."

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, safe_name)  # Build path safely
    file.save(save_path)

    # Operational hardening tip (outside Python):
    # configure your web server so /uploads is static-only (no script execution).
    return f"File {safe_name} uploaded safely."


# --- (Optional) Local demo harness to mirror the tutorial style ---
class MockFile:
    def __init__(self, name):
        self.filename = name
    def save(self, path):
        print(f"[SECURE] Saving to {path}")

if __name__ == "__main__":
    # Try names like: "cat.png" (allowed) vs "shell.php" (should be blocked)
    user_file = MockFile(input("Enter filename: "))
    print(upload_file_secure(user_file))
