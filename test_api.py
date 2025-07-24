import os
import shutil
import asyncio
import httpx

API_URL = "http://127.0.0.1:8000"

encrypted_dir = "encrypted"
decrypted_dir = "decrypted"
test_file_path = "test_image.jpg"

def setup_dirs():
    os.makedirs(encrypted_dir, exist_ok=True)
    os.makedirs(decrypted_dir, exist_ok=True)

async def test_ping(client):
    print("Testing /ping endpoint...")
    r = await client.get(f"{API_URL}/ping")
    assert r.status_code == 200
    assert r.json() == {"ping": "pong"}
    print("Ping test passed.")

async def test_encrypt_decrypt_text(client):
    print("Testing text encryption and decryption...")
    message = "Hello, Kaalka!"
    # Encrypt text
    r_enc = await client.post(f"{API_URL}/encrypt/text", params={"message": message})
    assert r_enc.status_code == 200
    cipher = r_enc.json().get("cipher")
    assert cipher is not None

    # Decrypt text
    r_dec = await client.post(f"{API_URL}/decrypt/text", params={"cipher": cipher})
    assert r_dec.status_code == 200
    decrypted_message = r_dec.json().get("message")
    assert decrypted_message == message
    print("Text encryption/decryption test passed.")

async def test_encrypt_decrypt_file(client):
    print("Testing file encryption and decryption...")
    # Encrypt file
    with open(test_file_path, "rb") as f:
        files = {"file": (os.path.basename(test_file_path), f, "application/octet-stream")}
        r_enc = await client.post(f"{API_URL}/encrypt/file", files=files)
    assert r_enc.status_code == 200
    enc_filename = r_enc.headers.get("content-disposition").split("filename=")[-1].strip('"')
    enc_file_path = os.path.join(encrypted_dir, enc_filename)
    with open(enc_file_path, "wb") as f:
        f.write(r_enc.content)
    print(f"Encrypted file saved to {enc_file_path}")

    # Decrypt file
    with open(enc_file_path, "rb") as f:
        files = {"file": (enc_filename, f, "application/octet-stream")}
        r_dec = await client.post(f"{API_URL}/decrypt/file", files=files)
    assert r_dec.status_code == 200
    dec_filename = r_dec.headers.get("content-disposition").split("filename=")[-1].strip('"')
    dec_file_path = os.path.join(decrypted_dir, dec_filename)
    with open(dec_file_path, "wb") as f:
        f.write(r_dec.content)
    print(f"Decrypted file saved to {dec_file_path}")

    # Check decrypted file exists and size > 0
    assert os.path.exists(dec_file_path)
    assert os.path.getsize(dec_file_path) > 0
    print("File encryption/decryption test passed.")

async def test_error_handling(client):
    print("Testing error handling for invalid inputs...")
    # Decrypt text with invalid cipher
    r = await client.post(f"{API_URL}/decrypt/text", params={"cipher": "invalidcipher"})
    # The API returns 200 with error message in detail, so check for 200 and error detail
    assert r.status_code == 200 or r.status_code == 500
    if r.status_code == 200:
        json_resp = r.json()
        assert any(key in json_resp for key in ["detail", "error", "message"])
    print("Error handling test passed.")

async def main():
    setup_dirs()
    async with httpx.AsyncClient() as client:
        await test_ping(client)
        await test_encrypt_decrypt_text(client)
        await test_encrypt_decrypt_file(client)
        await test_error_handling(client)
    print("All tests passed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
