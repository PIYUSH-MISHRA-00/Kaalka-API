from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from datetime import datetime
from models import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse, EncryptFileResponse, DecryptFileResponse
from utils import encrypt, decrypt

app = FastAPI(title="Kaalka API", description="Time-based encryption API using Kaalka library", version="1.0.0")

# Middleware to ignore unexpected headers from RapidAPI
@app.middleware("http")
async def ignore_rapidapi_headers(request: Request, call_next):
    # List of headers to ignore
    headers_to_ignore = {
        "host",
        "x-amzn-trace-id",
        "x-forwarded-port",
        "sec-fetch-site",
        "x-rapidapi-key",
        "cache-control",
        "referer",
        "csrf-token",
        "x-rapidapi-host",
        "origin",
        "expires",
        "accept",
        "usequerystring",
        "x-forwarded-proto",
        "priority",
        "x-forwarded-for",
        "x-rapidapi-ua",
        "sec-fetch-dest",
        "pragma",
        "rapid-client",
        "accept-language",
        "x-correlation-id",
        "x-entity-id"
    }
    # Since request.headers is immutable, create a new headers dict excluding unwanted headers
    new_headers = {k: v for k, v in request.headers.items() if k.lower() not in headers_to_ignore}
    # Create a new request with filtered headers
    request._headers = new_headers  # Note: This is a hack; better to handle differently if possible
    response = await call_next(request)
    return response

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

# Exception handler for general exceptions with logging
import logging

logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
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
