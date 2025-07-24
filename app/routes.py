from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from .kaalka_wrapper import (
    encrypt_text, decrypt_text,
    encrypt_file, decrypt_file,
    encrypt_file_bytes, decrypt_file_bytes
)
import tempfile
import os
import io

router = APIRouter()

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@router.get("/ping")
async def ping():
    return {"ping": "pong"}

@router.post("/encrypt")
async def encrypt_endpoint(
    message: str = Form(None),
    file: UploadFile = File(None),
    time_key: str = Form(None)
):
    try:
        if message is not None:
            # Encrypt text
            cipher = encrypt_text(message, time_key)
            return {"cipher": cipher}
        elif file is not None:
            # Encrypt file
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp.flush()
                enc_path = encrypt_file(tmp.name, time_key=time_key)
            with open(enc_path, "rb") as f:
                encrypted_data = f.read()
            task = BackgroundTask(remove_file, tmp.name)
            # Removed invalid add_task call
            enc_filename = os.path.basename(enc_path)
            return StreamingResponse(io.BytesIO(encrypted_data), media_type="application/octet-stream",
                                     headers={"Content-Disposition": f"attachment; filename={enc_filename}"},
                                     background=task)
        else:
            raise HTTPException(status_code=400, detail="Either message or file must be provided for encryption.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decrypt")
async def decrypt_endpoint(
    cipher: str = Form(None),
    file: UploadFile = File(None),
    time_key: str = Form(None)
):
    try:
        if cipher is not None:
            # Decrypt text
            plain = decrypt_text(cipher, time_key)
            return {"message": plain}
        elif file is not None:
            # Decrypt file using decrypt_file to get decrypted file path with original extension
            suffix = os.path.splitext(file.filename)[1]
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
                tmp_in.write(await file.read())
                tmp_in.flush()
                dec_path = decrypt_file(tmp_in.name, output_dir=tempfile.gettempdir(), time_key=time_key)
            def cleanup():
                try:
                    os.remove(tmp_in.name)
                except Exception:
                    pass
                try:
                    os.remove(dec_path)
                except Exception:
                    pass
            from starlette.background import BackgroundTask
            dec_filename = os.path.basename(dec_path)
            from fastapi.responses import FileResponse
            return FileResponse(dec_path, filename=dec_filename, background=BackgroundTask(cleanup))
        else:
            raise HTTPException(status_code=400, detail="Either cipher or file must be provided for decryption.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
