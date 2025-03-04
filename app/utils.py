import os

def cleanup_files(*files):
    """Removes specified files if they exist."""
    for file in files:
        if file and os.path.exists(file):
            os.remove(file)