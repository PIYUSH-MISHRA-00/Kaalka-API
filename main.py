from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from datetime import datetime
from models import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse
from utils import encrypt, decrypt

app = FastAPI(title="Kaalka API", description="Time-based encryption API using Kaalka library", version="1.0.0")

# Configure CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

@app.get("/ping")
async def ping():
    return {"message": "Kaalka API is running"}

@app.post("/encrypt", response_model=EncryptResponse)
async def encrypt_endpoint(request: EncryptRequest):
    timestamp = request.timestamp
    if not timestamp:
        timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        encrypted = encrypt(request.message, timestamp)
        return EncryptResponse(encrypted=encrypted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decrypt", response_model=DecryptResponse)
async def decrypt_endpoint(request: DecryptRequest):
    try:
        decrypted = decrypt(request.encrypted, request.timestamp)
        return DecryptResponse(decrypted=decrypted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
