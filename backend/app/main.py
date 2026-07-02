from fastapi import FastAPI

from app.api.v1 import api_router

app = FastAPI(title="Kọ́mi API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")


@app.get("/", summary="Root")
async def root():
    return {"message": "Welcome to Kọ́mi backend"}
