import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_ping():
    resp = requests.get(f"{BASE_URL}/ping")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Kaalka API is running"}
    print("GET /ping passed")

def test_encrypt_decrypt():
    timestamp = "12:00:00"
    message = "hello world"
    # Encrypt
    resp = requests.post(f"{BASE_URL}/encrypt", json={"message": message, "timestamp": timestamp})
    assert resp.status_code == 200
    encrypted = resp.json().get("encrypted")
    assert encrypted is not None and len(encrypted) > 0
    print("POST /encrypt passed")

    # Decrypt
    resp = requests.post(f"{BASE_URL}/decrypt", json={"encrypted": encrypted, "timestamp": timestamp})
    assert resp.status_code == 200
    decrypted = resp.json().get("decrypted")
    assert decrypted == message
    print("POST /decrypt passed")

def test_encrypt_without_timestamp():
    message = "test message"
    resp = requests.post(f"{BASE_URL}/encrypt", json={"message": message})
    assert resp.status_code == 200
    encrypted = resp.json().get("encrypted")
    assert encrypted is not None and len(encrypted) > 0
    print("POST /encrypt without timestamp passed")

def test_missing_fields():
    # Missing message in encrypt
    resp = requests.post(f"{BASE_URL}/encrypt", json={})
    assert resp.status_code == 422
    print("POST /encrypt missing message field passed")

    # Missing encrypted in decrypt
    resp = requests.post(f"{BASE_URL}/decrypt", json={"timestamp": "12:00:00"})
    assert resp.status_code == 422
    print("POST /decrypt missing encrypted field passed")

    # Missing timestamp in decrypt
    resp = requests.post(f"{BASE_URL}/decrypt", json={"encrypted": "abc"})
    assert resp.status_code == 422
    print("POST /decrypt missing timestamp field passed")

def test_invalid_timestamp():
    # Invalid timestamp format in encrypt
    resp = requests.post(f"{BASE_URL}/encrypt", json={"message": "test", "timestamp": "invalid"})
    assert resp.status_code == 500
    print("POST /encrypt invalid timestamp passed")

    # Invalid timestamp format in decrypt
    resp = requests.post(f"{BASE_URL}/decrypt", json={"encrypted": "abc", "timestamp": "invalid"})
    assert resp.status_code == 500
    print("POST /decrypt invalid timestamp passed")

def test_empty_message_and_encrypted():
    # Empty message encrypt
    resp = requests.post(f"{BASE_URL}/encrypt", json={"message": ""})
    assert resp.status_code == 200
    print("POST /encrypt empty message passed")

    # Empty encrypted decrypt
    resp = requests.post(f"{BASE_URL}/decrypt", json={"encrypted": "", "timestamp": "12:00:00"})
    assert resp.status_code == 200
    print("POST /decrypt empty encrypted passed")

if __name__ == "__main__":
    test_ping()
    test_encrypt_decrypt()
    test_encrypt_without_timestamp()
    test_missing_fields()
    test_invalid_timestamp()
    test_empty_message_and_encrypted()
    print("All tests passed successfully.")
