from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file):
    filename = secure_filename(file.filename)

    if not is_allowed(filename):
        return "File type not allowed"

    save_path = os.path.join("uploads", filename)
    file.save(save_path)
    return f"File {filename} uploaded safely"
