from pydantic import BaseModel, Field
from typing import Optional

class EncryptRequest(BaseModel):
    message: str = Field(..., description="The message to encrypt")
    timestamp: Optional[str] = Field(None, description="Optional timestamp in HH:MM:SS format")

class EncryptResponse(BaseModel):
    encrypted: str = Field(..., description="The encrypted message")

class DecryptRequest(BaseModel):
    encrypted: str = Field(..., description="The encrypted message to decrypt")
    timestamp: str = Field(..., description="Timestamp in HH:MM:SS format")

class DecryptResponse(BaseModel):
    decrypted: str = Field(..., description="The decrypted message")
