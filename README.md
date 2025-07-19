# Kaalka API

![Kaalka API](https://img.shields.io/badge/Kaalka-API-blue?style=for-the-badge\&logo=fastapi)

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
uvicorn main:app --reload
```

Visit your API at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧩 API Endpoints

### 🔒 POST `/encrypt`

Encrypt a message using optional timestamp.

#### Request Body:

```json
{
  "message": "string",
  "timestamp": "optional, string in HH:MM:SS"
}
```

#### Response:

```json
{
  "encrypted": "string"
}
```

📌 *If `timestamp` is omitted, system time is used.*

---

### 🔓 POST `/decrypt`

Decrypt a message using the required timestamp.

#### Request Body:

```json
{
  "encrypted": "string",
  "timestamp": "required, string in HH:MM:SS"
}
```

#### Response:

```json
{
  "decrypted": "string"
}
```

---

### ✅ GET `/ping`

Health check for the API.

#### Response:

```json
{
  "message": "Kaalka API is running"
}
```

---

## 🔁 Usage Examples

### 🔐 Encrypt (cURL)

**PowerShell:**

```powershell
curl -Method POST http://localhost:8000/encrypt -Headers @{"Content-Type" = "application/json"} -Body '{"message": "hello world", "timestamp": "12:00:00"}'
```

**Bash:**

```bash
curl -X POST http://localhost:8000/encrypt \
-H "Content-Type: application/json" \
-d '{"message":"hello world","timestamp":"12:00:00"}'
```

### 🔓 Decrypt (cURL)

**PowerShell:**

```powershell
curl -Method POST http://localhost:8000/decrypt -Headers @{"Content-Type" = "application/json"} -Body '{"encrypted": "<encrypted_string>", "timestamp": "<timestamp>"}'
```

**Bash:**

```bash
curl -X POST http://localhost:8000/decrypt \
-H "Content-Type: application/json" \
-d '{"encrypted":"<encrypted_string>","timestamp":"<timestamp>"}'
```

---

### 🧪 Test With Postman

1. Open [Postman](https://www.postman.com/)
2. Create a new `POST` request:

   * URL: `http://localhost:8000/encrypt`
   * Headers: `Content-Type: application/json`
   * Body (raw, JSON):

     ```json
     {
       "message": "hello world",
       "timestamp": "12:00:00"
     }
     ```
3. Create another `POST` request to `/decrypt` similarly with the following body format:

     ```json
     {
       "encrypted": "<encrypted_string>",
       "timestamp": "12:00:00"
     }
     ```

✅ You can also import OpenAPI spec from `/openapi.json` in Postman.
     }

---

## 🧪 Testing

A `test_api.py` script is included with unit and integration tests.

Run tests:

```bash
python test_api.py
```

Tests include:

* ✅ GET /ping
* 🔐 POST /encrypt
* 🔓 POST /decrypt
* ❌ Edge cases: missing/invalid input

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

Build and run:

```bash
docker build -t kaalka-api .
docker run -p 80:80 kaalka-api
```

### Cloud Hosting

You can deploy to:

* [Render](https://render.com/)
* [Railway](https://railway.app/)
* [Fly.io](https://fly.io/)
* [Vercel](https://vercel.com/) *(via serverless)*

---

## 💡 Notes

* The API uses the [`kaalka`](https://pypi.org/project/kaalka/) library via `pip install kaalka`
* Fully stateless – all data is processed per request
* Modular and extendable design

---
[Docker Image](https://hub.docker.com/r/piyushmishradocker/kaalka-api)
