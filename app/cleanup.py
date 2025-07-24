import os
import time
import threading

TEMP_DIR = "/tmp"  # Adjust this path as needed for your environment
EXTENSIONS_TO_CLEAN = [".kaalka", ".kaalka.debug_orig"]
AGE_THRESHOLD_SECONDS = 60  # 1 minute

def cleanup_temp_files():
    while True:
        now = time.time()
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                if any(file.endswith(ext) for ext in EXTENSIONS_TO_CLEAN):
                    file_path = os.path.join(root, file)
                    try:
                        file_age = now - os.path.getmtime(file_path)
                        if file_age > AGE_THRESHOLD_SECONDS:
                            os.remove(file_path)
                            print(f"Deleted temp file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
        time.sleep(AGE_THRESHOLD_SECONDS)

def start_cleanup_loop():
    thread = threading.Thread(target=cleanup_temp_files, daemon=True)
    thread.start()
