import os
import tempfile
from kaalka import Kaalka

kaalka = Kaalka()

def encrypt_text(message: str, time_key: str = None) -> str:
    if time_key:
        kaalka.time_key = time_key
        result = kaalka.encrypt(message)
        kaalka.time_key = None
        return result
    return kaalka.encrypt(message)

def decrypt_text(cipher: str, time_key: str = None) -> str:
    if time_key:
        kaalka.time_key = time_key
        result = kaalka.decrypt(cipher)
        kaalka.time_key = None
        return result
    return kaalka.decrypt(cipher)

def encrypt_file(input_path: str, output_dir: str = '.', time_key: str = None) -> str:
    if time_key:
        kaalka.time_key = time_key
        encrypted_path = kaalka.encrypt(input_path)
        kaalka.time_key = None
    else:
        encrypted_path = kaalka.encrypt(input_path)
    if output_dir != '.':
        os.replace(encrypted_path, os.path.join(output_dir, os.path.basename(encrypted_path)))
        encrypted_path = os.path.join(output_dir, os.path.basename(encrypted_path))
    return encrypted_path

import time
def encrypt_file_bytes(file_bytes: bytes, time_key: str = None) -> bytes:
    import os
    import tempfile
    import time
    if time_key:
        kaalka.time_key = time_key
    else:
        kaalka.time_key = None
    with tempfile.NamedTemporaryFile(delete=True) as tmp_in:
        tmp_in.write(file_bytes)
        tmp_in.flush()
        encrypted_path = kaalka.encrypt(tmp_in.name)
        with open(encrypted_path, "rb") as f:
            encrypted_bytes = f.read()
        # Wait briefly to ensure kaalka finishes writing files
        time.sleep(0.5)
        # Remove encrypted file and any .kaalka.debug_orig files with retries
        for path in [encrypted_path, encrypted_path + ".debug_orig"]:
            for _ in range(3):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        break
                except Exception as e:
                    time.sleep(0.1)
    return encrypted_bytes

def decrypt_file(input_path: str, output_dir: str = '.', time_key: str = None) -> str:
    if time_key:
        kaalka.time_key = time_key
        decrypted_path = kaalka.decrypt(input_path)
        kaalka.time_key = None
    else:
        decrypted_path = kaalka.decrypt(input_path)
    if output_dir != '.':
        os.replace(decrypted_path, os.path.join(output_dir, os.path.basename(decrypted_path)))
        decrypted_path = os.path.join(output_dir, os.path.basename(decrypted_path))
    return decrypted_path

def encrypt_file_bytes(file_bytes: bytes, time_key: str = None) -> bytes:
    if time_key:
        kaalka.time_key = time_key
    else:
        kaalka.time_key = None
    with tempfile.NamedTemporaryFile(delete=True) as tmp_in:
        tmp_in.write(file_bytes)
        tmp_in.flush()
        encrypted_path = kaalka.encrypt(tmp_in.name)
        with open(encrypted_path, "rb") as f:
            encrypted_bytes = f.read()
        os.remove(encrypted_path)
    return encrypted_bytes

def decrypt_file_bytes(file_bytes: bytes, time_key: str = None) -> bytes:
    if time_key:
        kaalka.time_key = time_key
    else:
        kaalka.time_key = None
    with tempfile.NamedTemporaryFile(delete=True) as tmp_in:
        tmp_in.write(file_bytes)
        tmp_in.flush()
        decrypted_path = kaalka.decrypt(tmp_in.name)
        with open(decrypted_path, "rb") as f:
            decrypted_bytes = f.read()
        os.remove(decrypted_path)
    return decrypted_bytes
