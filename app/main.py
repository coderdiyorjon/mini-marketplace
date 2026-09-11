from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import Database
from app.api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    yield
    await Database.disconnect()

app = FastAPI(
    title="Mini Marketplace API",
    lifespan=lifespan
)

app.include_router(auth_router)

@app.get("/health")
async def health_check():
    return {"status": "Databse connects automaticaly"}