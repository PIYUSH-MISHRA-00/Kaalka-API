from fastapi import FastAPI
from .routes import router
from .cleanup import start_cleanup_loop

app = FastAPI(title="Kaalka Encryption API")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    start_cleanup_loop()
