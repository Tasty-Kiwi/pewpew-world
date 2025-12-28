import uvicorn
from app.api.v1 import router as v1_router
from fastapi import FastAPI

app = FastAPI(title="PewPew World API", version="1.0.0")

app.include_router(v1_router, prefix="/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
