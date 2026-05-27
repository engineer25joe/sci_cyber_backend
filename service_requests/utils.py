import os


def validate_file_size(file, max_size=100 * 1024 * 1024):
    return file.size <= max_size


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def is_allowed_file(filename):
    allowed = [
        ".pdf", ".doc", ".docx",
        ".jpg", ".jpeg", ".png",
        ".zip", ".txt"
    ]
    return get_file_extension(filename) in allowed
