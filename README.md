# Kaalka Encryption API

A FastAPI wrapper over the time-based Kaalka Encryption algorithm supporting:

- `GET /ping`: health check.
- `POST /encrypt/text`: text encryption, returns JSON `{ "cipher": ... }`.
- `POST /decrypt/text`: text decryption, returns `{ "message": ... }`.
- `POST /encrypt/file`: upload any file, returns `.kaalka` encrypted file.
- `POST /decrypt/file`: upload `.kaalka`, returns decrypted original file.

### Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ensure that a Python Kaalka package compatible with the Rust/Dart library is available from PyPI or GitHub.

---

## How It Works

- **Text endpoints** accept strings and optional `time_key` (if using non-current timestamp), returning JSON.
- **File endpoints** accept uploads, feed them to `kaalka.encrypt()`/`decrypt()`, then return the resulting file under `.kaalka` or original extension.
- **`/ping`** verifies server availability.

This implementation follows the described behavior of the Dart library—timestamp-based encryption, `.kaalka` extension handling, cross-language compatibility.
