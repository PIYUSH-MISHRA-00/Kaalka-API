# Kaalka API

![Kaalka API](https://img.shields.io/badge/Kaalka-API-blue?style=for-the-badge&logo=fastapi)

## 🌐 Overview

**Kaalka API** is a modern, time-based encryption and decryption RESTful service built using **FastAPI**, powered by the [Kaalka](https://pypi.org/project/kaalka/) encryption library. This API enables developers and businesses to secure messages using timestamps with simple HTTP requests.

---

## ✨ Features

* 🔐 **Time-based encryption & decryption** using `kaalka`
* 🚀 **FastAPI-powered**, blazing fast and async-ready
* 📄 **Interactive Swagger Docs** at `/docs`
* 🌍 **CORS** enabled for all origins
* 🛡️ **Input validation** and structured error handling
* 📦 **Ready for deployment**: local, cloud, Docker
* 🆕 **In-memory streaming** of file uploads/downloads to avoid persistent server storage
* 🆕 **Automatic restoration** of original file extensions on decrypted files
* 🆕 **Background cleanup** of temporary encrypted and debug files every 60 seconds
* 🆕 **Streamlit app** for easy testing of API endpoints and file operations

---

## 🧩 Project Structure

```
kaalka_api/
├── app/
│   ├── main.py           # FastAPI app declaration and cleanup integration
│   ├── routes.py         # API endpoints for encryption/decryption
│   ├── kaalka_wrapper.py # Python wrapper around Kaalka library
│   └── cleanup.py        # Background cleanup logic for temporary files
├── requirements.txt
├── README.md
└── streamlit_test_app.py # Streamlit app for testing the API
```

---

## 📥 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PIYUSH-MISHRA-00/Kaalka-API.git
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Visit your API at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testing

You can test the API endpoints using tools like Curl or Postman.

### API Endpoints

- `GET /ping`: Health check.
- `POST /encrypt`: Encrypt text or file. Supports optional `time_key`.
- `POST /decrypt`: Decrypt text or file. Supports optional `time_key`.

### Example Curl Requests

**Encrypt text:**

```bash
curl -X POST http://localhost:8000/encrypt \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "message=hello world&time_key=12:00:00"
```

**Decrypt text:**

```bash
curl -X POST http://localhost:8000/decrypt \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "cipher=<encrypted_string>&time_key=12:00:00"
```

**Encrypt file:**

```bash
curl -X POST http://localhost:8000/encrypt \
-F "file=@path/to/file" \
-F "time_key=12:00:00"
```

**Decrypt file:**

```bash
curl -X POST http://localhost:8000/decrypt \
-F "file=@path/to/file.kaalka" \
-F "time_key=12:00:00"
```

---

## 🧑‍💻 Streamlit Test App

Run the Streamlit app for easy testing of the API:

```bash
streamlit run streamlit_test_app.py
```

---

## 🛠️ Cleanup of Temporary Files

The Kaalka library writes temporary encrypted files and debug files during encryption. These files are automatically cleaned up every 60 seconds by a background task integrated into the FastAPI app.

---

## 🚢 Deployment

### Using Docker

**Dockerfile**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

Build and run:

```bash
docker build -t kaalka-api .
docker run -p 80:80 kaalka-api
```

---

## 💡 Notes

* Fully stateless – all data is processed per request
* Modular and extendable design

---
